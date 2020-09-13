from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import PsyxDB
from PsyxDB import Tool
import sys, os, shutil, random, json
from werkzeug.utils import secure_filename

api = Flask(__name__)
CORS(api)
api.debug = True


# @api.route('/admin/login', method=['POST'])
# def login():
#     return True


@api.route('/admin/list', methods=['GET']) # FIXME: null to 0
def list_packs():
    print('\n * ',sys._getframe().f_code.co_name)
    result = {}
    packs = PsyxDB.get_all_packs()
    result['pack_num'] = len(packs)
    result['pack_list'] = packs
    return jsonify(result)


@api.route('/admin/create', methods=['POST']) # FORM
def create_pack():
    print('\n * ',sys._getframe().f_code.co_name)
    # check if the post request has the file part
    if 'file' not in request.files:
        return 'Nothing Uploaded'
    # get other args
    pack_name = request.form.get('pack_name', type=str)
    if Tool._check_pack_name(pack_name) != True:
        return 'Invalid Pack Name'
    age_lower = request.form.get('age_lower', type=int)
    age_upper = request.form.get('age_upper', type=int)
    if not Tool.check_age(age_lower) or not Tool.check_age(age_upper): # TODO: check age_bound()
        return 'Invalid Age Bound'
    sex = int(request.form.get('sex', type=str))
    if Tool.check_sex(sex) == False:
        return 'Invalid Sex'
    print('\t* sex:', sex)
    print('\t* age:', age_lower, '~', age_upper)
    print('\t* pack_name:', pack_name)

    # check if there's any folder with the same name
    UPLOAD_FOLDER = '/home/xmx1025/Psyx/packs' # TODO: use config
    dst_path = os.path.join(UPLOAD_FOLDER, pack_name)
    if os.path.exists(dst_path):
        return 'pack existed' # TODO: return error code?
    os.makedirs(dst_path)

    # put this two functions to the Tool class
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    def absorb_filename(filename):
        return filename.split(os.sep)[-1]
    
    for f in request.files.getlist('file'):
        print('file part =', type(f))
        print(f)
        # if user does not select file, browser also
        # submit an empty part without filename
        if f.filename == '':
            return 'No selected file'
        if f and allowed_file(f.filename):
            filename = secure_filename(absorb_filename(f.filename))
            print('name :', filename)
            f.save(os.path.join(dst_path, filename))

    # add to db
    p_id = PsyxDB.add_pack(sex=sex, age_lower=age_lower, age_upper=age_upper, pack_name=pack_name)
    if p_id == 0:
        # TODO: delete folder
        return 'failed to add to db'
    return 'Pack ' + str(p_id) + ' Added.'


@api.route('/admin/remove', methods=['GET']) # id
def remove_pack():
    print('\n * ',sys._getframe().f_code.co_name)
    # mv Pack Folder
    p_id = request.args.get('id', type=int)
    result = {
        'result' : 'failed'
    }
    pack_name = PsyxDB.delete_pack(p_id)
    if pack_name != None:
        pack_path = os.path.join(Tool.PACK_BASE_PATH, pack_name)
        print('\tRemove Pack')
        print('\t\t' + pack_path)
        if os.path.exists(pack_path) and os.path.isdir(pack_path) == True:
            shutil.rmtree(pack_path)
            result['result'] = 'succeed'
        else:
            result['message'] = 'ERROR: packbase damaged'
    else:
        result['message'] = 'p_id={} not found'.format(p_id)

    return jsonify(result)


@api.route('/admin/report', methods=['GET']) # id FIXME:
def report_pack():
    print('\n * ',sys._getframe().f_code.co_name)
    p_id = request.args.get('id', type=int)
    result = PsyxDB.get_all_replies(p_id)
    if result == None: # TODO: return
        result = {
            'result' : 'failed',
            'message' : 'No Replies Yet'
        }
    return jsonify(result)


@api.route('/reply/start', methods=['POST']) # FORM
def start_reply():
    print('\n * ',sys._getframe().f_code.co_name)
    # get inputs from form
    data = request.get_json()
    # print(data) # FIXME: why why why
    # data = json.loads(data)
    print(data)
    name = data['name']
    email = data['email']
    no = data['no']
    sex = data['sex']
    age = data['age']
    phone = data['phone']
    print(' * Testing args..')
    print('\t', name)
    print('\t', email)
    print('\t', sex)
    print('\t', age)
    print('\t', no)
    print('\t', phone)

    # check inputs
    result = {
        'result' : 'failed'
    }
    if Tool.check_name(name) != True:
        result['message'] = str(name) + 'Invalid Name'
        return jsonify(result)
    if Tool.check_email(email) != True:
        result['message'] = str(email) + 'Invalid Email Address'
        return jsonify(result)
    if Tool.check_sex(sex) != True:
        result['message'] = str(sex) + 'Invalid Sex'
        return jsonify(result)
    if Tool.check_age(age) != True:
        result['message'] = str(age) + 'Invalid Age'
        return jsonify(result)
    if Tool.check_no(no) != True:
        result['message'] = str(no) + 'Invalid ExperimentNo.'
        return jsonify(result)
    if Tool.check_phone(phone) != True:
        result['message'] = str(phone) + 'Invalid Phone Number'
        return jsonify(result)

    # get pack path
    p_id, pack_name = PsyxDB.get_pack_path(sex=sex, age=age)
    if p_id == 0 or pack_name == None:
        result['message'] = 'None Suitable Pack'
    else:
        result['result'] = 'succeed'
        result['p_id'] = p_id
        result['pack_path'] = os.path.join('/packs', pack_name) # TODO: use condif
        pics = []
        for i in os.listdir(os.path.join(Tool.PACK_BASE_PATH, pack_name)):
            pics.append(i)
        pics.sort()
        pics_pairs = [pics[i:i+2] for i in range(0, len(pics), 2)]
        random.shuffle(pics_pairs)
        result['pic_pairs'] = pics_pairs

    return jsonify(result)


@api.route('/reply/submit', methods=['POST']) # JSON
def submit_reply():
    print('\n * ',sys._getframe().f_code.co_name)
    data = request.get_json() # TODO: force=True?
    print(data)
    p_id = data['p_id']
    name = data['name']
    email = data['email']
    no = data['no']
    sex = data['sex']
    age = data['age']
    phone = data['phone']
    answers = data['answers']

    result = {
        'result' : 'failed'
    }
    if PsyxDB.add_reply(p_id=p_id, name=name, email=email, no=no, sex=sex,
                        age=age, phone=phone, answers=answers) == True:
        result['result'] = 'succeed'

    return jsonify(result)
