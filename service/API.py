from flask import Flask, Response, request, jsonify, abort
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

# TODO: use this one to response error
@api.errorhandler(418)
def handle_client_error(msg):
    result = '< CLIENT ERROR > %s' % msg
    print(result)
    return result, 418

@api.errorhandler(500)
def handle_server_error(msg):
    result = '< SERVER ERROR > %s' % msg
    print(result)
    return result, 500


@api.route('/admin/list', methods=['GET']) # FIXME: null to 0
def list_packs():
    print('\n * ',sys._getframe().f_code.co_name)
    result = PsyxDB.get_all_packs()
    if (result == None):
        abort(500, 'Failed To Read From DB')
    for each in result:
        if (each['count'] == None):
            each['count'] = 0
    print(result)
    return jsonify(result)


@api.route('/admin/create', methods=['POST']) # FORM
def create_pack():
    print('\n * ',sys._getframe().f_code.co_name)
    # check if the post request has the file part
    if 'file' not in request.files:
        abort(418, 'Nothing Uploaded')
    # get other args
    pack_name = request.form.get('pack_name', type=str)
    if not Tool.check_pack_name(pack_name):
        abort(418, 'Invalid Pack Name')
    age_lower = request.form.get('age_lower', type=int)
    age_upper = request.form.get('age_upper', type=int)
    if not Tool.check_age(age_lower) or not Tool.check_age(age_upper) or age_lower > age_upper:
        abort(418, 'Invalid Age Bound')
    sex = int(request.form.get('sex', type=str))
    if Tool.check_sex(sex) == False:
        abort(418, 'Invalid Sex')
    print('\t* sex:', sex)
    print('\t* age:', age_lower, '~', age_upper)
    print('\t* pack_name:', pack_name)

    # check if there's any folder with the same name
    UPLOAD_FOLDER = '/home/xmx1025/Psyx/packs' # TODO: use config
    dst_path = os.path.join(UPLOAD_FOLDER, pack_name)
    if not os.path.exists(UPLOAD_FOLDER):
        abort(500, 'Packbase Damaged!')
    if os.path.exists(dst_path):
        abort(418, 'Pack Existed')
    
    files = [] # [(f0, n0), (f1, n1), (f2, n2), ...], f for file, n for filename
    for f in request.files.getlist('file'):
        if f.filename == '':
            # if user does not select file, browser also submit an empty part without filename
            abort(418, 'No Selected File')
        if f and Tool.check_file_type(f.filename): # FIXME: why keep failed here?
            n = secure_filename(Tool.absorb_filename(f.filename))
            if Tool.check_file_name(n):
                files.append((f, n))
            else:
                abort(418, 'Invalid File Or Invalid Filename: %s' % n)
        else:
            abort(418, 'Invalid File Type')

    # make pack folder and save files
    if (len(files) == Tool.PACK_SIZE):
        print('\t * making pack..')
        os.makedirs(dst_path)
        for f, n in files: # f for file, n for filename
            f.save(os.path.join(dst_path, n)) # TODO: if failed to save?
    else:
        abort(418, 'Invalid Folder Size')

    # add to db
    p_id = PsyxDB.add_pack(sex=sex, age_lower=age_lower, age_upper=age_upper, pack_name=pack_name)
    if p_id == 0:
        # TODO: delete folder
        abort(500, 'Failed To Add To DB')
    return 'Pack ' + str(p_id) + ' Added.' # TODO: is this json?


@api.route('/admin/remove', methods=['GET']) # id
def remove_pack():
    print('\n * ',sys._getframe().f_code.co_name)
    # mv Pack Folder
    p_id = request.args.get('id', type=int)
    pack_name = PsyxDB.delete_pack(p_id)
    if pack_name != None:
        pack_path = os.path.join(Tool.PACK_BASE_PATH, pack_name)
        print('\tRemoving Pack', pack_path, '..')
        if os.path.exists(pack_path) and os.path.isdir(pack_path) == True:
            shutil.rmtree(pack_path)
        else:
            abort(500, 'Packbase Damaged!')
    else:
        abort(418, 'Pack %s Not Found' % p_id)

    return 'Pack ' + str(p_id) + ' Deleted.' # TODO: is this json?


@api.route('/admin/download', methods=['GET']) # id
def download_pack():
    print('\n * ',sys._getframe().f_code.co_name)
    p_id = request.args.get('id', type=int)
    # TODO: if unknown p_id??
    replies = PsyxDB.get_all_replies(p_id) # a list of dictionaries (each dic is a record in db)
    result = { # TODO: add pack info to result
        'set' : 'example',
        'age_lower' : 0,
        'age_upper' : 120,
        'sex' : 1,
        'date' : '2020.09.18 20:36:47',
        'replies' : []
    }
    if (replies != None):
        result['replies'] = replies
    return jsonify(result)


@api.route('/reply/start', methods=['POST']) # FORM
def start_reply():
    print('\n * ',sys._getframe().f_code.co_name)
    data = request.get_json()
    print(data)
    name = data['name']
    email = data['email']
    no = data['no']
    sex = data['sex']
    age = data['age']
    phone = data['phone']
    print('\t * Testing args..')

    # check inputs
    if Tool.check_name(name) != True:
        abort(418, 'Invalid Name: %s' % name)
    if Tool.check_email(email) != True:
        abort(418, 'Invalid Email Address: %s' % email)
    if Tool.check_sex(sex) != True:
        abort(418, 'Invalid Sex: %s' % sex)
    if Tool.check_age(age) != True:
        abort(418, 'Invalid Age: %s' % age)
    if Tool.check_no(no) != True:
        abort(418, 'Invalid ExperimentNo.: %s' % no)
    if Tool.check_phone(phone) != True:
        abort(418, 'Invalid Phone Number: %s' % phone)

    # get pack path # FIXME: check the return value
    p_id, pack_name = PsyxDB.get_pack_path(sex=sex, age=age)
    if p_id == 0 or pack_name == None:
        abort(418, 'None Suitable Pack') # TODO: not an error actually
    else:
        result = {}
        result['p_id'] = p_id
        result['pack_path'] = os.path.join('/packs', pack_name) # TODO: use config
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

    if PsyxDB.add_reply(p_id=p_id, name=name, email=email, no=no, sex=sex,
                        age=age, phone=phone, answers=answers) != True:
        abort(418, 'Failed To Submit Your Reply')

    return 'Reply Submited.'
