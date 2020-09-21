from flask import Flask, Response, request, jsonify, abort
from flask_cors import CORS
import PsyxDB
from PsyxDB import Tool
import os, shutil, random, json, re
from werkzeug.utils import secure_filename
from enum import Enum, unique
import logging
from logging.handlers import TimedRotatingFileHandler

"""
TODO:
 - clear comments
 - check import
 - disable CORS and DEBUG (but open CORS for download api?)
 - custom error description using Response?
 - add comments for every re patterns
 - date format?
"""

api = Flask(__name__)
CORS(api)


# set logger
log_name = 'api'
log_format = '[%(asctime)s * %(levelname)s]\t%(lineno)d \t%(funcName)s: %(message)s'
log_path = os.path.join(Tool.LOGBASE_PATH, log_name)
logger = logging.getLogger(log_name)
logger.setLevel(logging.INFO) # DEBUG < INFO < WARNING < ERROR < CRITICAL
# make one 1 log file every midnight, keep for 14 days
file_handler = TimedRotatingFileHandler(filename=log_path, when="MIDNIGHT", interval=1, backupCount=14)
file_handler.suffix = "%Y%m%d.log"
file_handler.extMatch = re.compile(r'^\d{8}.log$')
file_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(file_handler)


@unique
class STATUS(Enum):
    NO_SUITABLE_PACK = 404 # STATUS.NO_SUITABLE_PACK.value
    INVALID_INPUT = 400 # STATUS.INVALID_INPUT.value
    SERVER_ERROR = 500 # STATUS.SERVER_ERROR.value

# TODO: handle NO_SUITABLE PACK?

@api.errorhandler(STATUS.INVALID_INPUT.value)
def handle_invalid_input(msg):
    logger.warning(request.headers['X-Real-IP'])
    logger.warning(' - %s' % msg)
    return msg, STATUS.INVALID_INPUT.value

@api.errorhandler(STATUS.SERVER_ERROR.value)
def handle_server_error(msg):
    logger.error(request.headers['X-Real-IP'])
    logger.error(' - %s' % msg)
    result = '< SERVER ERROR > %s' % msg
    return result, STATUS.SERVER_ERROR.value


@api.route('/admin/list', methods=['GET'])
def list_packs():
    logger.info(request.headers['X-Real-IP'])
    result = PsyxDB.get_all_packs()
    for each in result: # the count will be null if that set hasn't received any replies
        if each['count'] is None:
            each['count'] = 0
    return jsonify(result)


@api.route('/admin/create', methods=['POST']) # FORM
def create_pack():
    logger.info(request.headers['X-Real-IP'])
    # check if the post request has the file part
    if 'file' not in request.files:
        abort(STATUS.INVALID_INPUT.value, 'Nothing Uploaded')
    # get other args
    pack_name = request.form.get('pack_name', type=str)
    if not Tool.check_pack_name(pack_name):
        abort(STATUS.INVALID_INPUT.value, 'Invalid Pack Name')
    age_min = request.form.get('age_min', type=int)
    age_max = request.form.get('age_max', type=int)
    if not Tool.check_age(age_min) or not Tool.check_age(age_max) or age_min > age_max:
        abort(STATUS.INVALID_INPUT.value, 'Invalid Age Bound')
    sex = int(request.form.get('sex', type=str))
    if Tool.check_sex(sex) == False:
        abort(STATUS.INVALID_INPUT.value, 'Invalid Sex')

    if not os.path.exists(Tool.PACKBASE_PATH):
        abort(STATUS.SERVER_ERROR.value, 'Packbase Damaged!')
    # check if there's any folder with the same name
    dst_path = os.path.join(Tool.PACKBASE_PATH, pack_name)
    if os.path.exists(dst_path):
        abort(STATUS.INVALID_INPUT.value, 'Pack Existed')
    
    files = [] # [(f0, n0), (f1, n1), (f2, n2), ...], f for file, n for filename
    for f in request.files.getlist('file'):
        if not f or f.filename == '':
            # if user does not select file, browser also submit an empty part without filename
            abort(STATUS.INVALID_INPUT.value, 'No Selected File')
        n = secure_filename(Tool.absorb_filename(f.filename))
        if Tool.check_file_name(n): # check for both file's type and name format
            files.append((f, n))
        else:
            logger.info(' - filtered file %s' % n)

    # make pack folder and save files
    if (len(files) == Tool.PACK_SIZE * 2):
        logger.info(' - making pack %s..' % dst_path)
        try:
            os.makedirs(dst_path)
            for f, n in files: # f for file, n for filename
                try:
                    f.save(os.path.join(dst_path, n))
                except:
                    shutil.rmtree(dst_path)
                    abort(STATUS.SERVER_ERROR.value, 'Server Failed to Save Files')
        except:
            abort(STATUS.SERVER_ERROR.value, 'Server Failed to Make Folder')
    else:
        abort(STATUS.INVALID_INPUT.value, 'Invalid Folder Size')

    # add to db
    p_id = PsyxDB.add_pack(sex=sex, age_min=age_min, age_max=age_max, pack_name=pack_name)
    if p_id == 0:
        shutil.rmtree(dst_path) # delete folder
        abort(STATUS.INVALID_INPUT.value, 'Pack Condition Overlapped')
    if p_id == -1:
        shutil.rmtree(dst_path) # delete folder
        abort(STATUS.SERVER_ERROR.value, 'Failed To Add To DB\n(check if there is a pack with the same name)')
    return 'Pack ' + str(p_id) + ' Added.'


@api.route('/admin/remove', methods=['GET']) # id
def remove_pack():
    logger.info(request.headers['X-Real-IP'])
    # mv Pack Folder
    p_id = request.args.get('id', type=int)
    pack_name = PsyxDB.delete_pack(p_id)
    if pack_name is not None:
        pack_path = os.path.join(Tool.PACKBASE_PATH, pack_name)
        logger.info(' - removing pack %s..' % pack_path)
        try:
            shutil.rmtree(pack_path)
        except:
            abort(STATUS.SERVER_ERROR.value, 'Packbase Damaged!')
    else:
        abort(STATUS.INVALID_INPUT.value, 'Unknown Pack %s' % p_id)

    return 'Pack ' + str(p_id) + ' Deleted.'


# TODO: @cross_origin()
@api.route('/admin/download', methods=['GET']) # id
def download_pack():
    logger.info(request.headers['X-Real-IP'])
    p_id = request.args.get('id', type=int)
    pack_info = PsyxDB.get_pack_info(p_id)
    if len(pack_info) == 0:
        abort(STATUS.INVALID_INPUT.value, 'Pack %s Not Found' % p_id)
    result = pack_info[0] # dict
    replies = PsyxDB.get_all_replies(p_id) # a list of dictionaries (each dic is a record in db)
    for r in replies:
        r['answers'] = json.loads(r['answers']) # the answers data in db is jsonstring
    result['replies'] = replies
    return jsonify(result)


@api.route('/reply/start', methods=['POST']) # FORM
def start_reply():
    logger.info(request.headers['X-Real-IP'])
    data = request.get_json()
    logger.debug(data)
    name = data['name']
    email = data['email']
    no = data['no']
    sex = data['sex']
    age = data['age']
    phone = data['phone']

    # check inputs
    if Tool.check_name(name) != True:
        abort(STATUS.INVALID_INPUT.value, 'Invalid Name: %s' % name)
    if Tool.check_email(email) != True:
        abort(STATUS.INVALID_INPUT.value, 'Invalid Email Address: %s' % email)
    if Tool.check_sex(sex) != True:
        abort(STATUS.INVALID_INPUT.value, 'Invalid Sex: %s' % sex)
    if Tool.check_age(age) != True:
        abort(STATUS.INVALID_INPUT.value, 'Invalid Age: %s' % age)
    if Tool.check_no(no) != True:
        abort(STATUS.INVALID_INPUT.value, 'Invalid ExperimentNo.: %s' % no)
    if Tool.check_phone(phone) != True:
        abort(STATUS.INVALID_INPUT.value, 'Invalid Phone Number: %s' % phone)

    p_id, pack_name = PsyxDB.get_pack_path(sex=sex, age=age)
    if p_id == 0 or pack_name is None:
        abort(STATUS.NO_SUITABLE_PACK.value, 'No Suitable Pack for You')
    else:
        result = {}
        result['p_id'] = p_id
        result['pack_path'] = Tool.PACKBASE_LOC + '/' + pack_name # TODO: check it at frontend
        pics = []
        for i in os.listdir(os.path.join(Tool.PACKBASE_PATH, pack_name)):
            pics.append(i)
        pics.sort()
        pics_pairs = [pics[i:i+2] for i in range(0, len(pics), 2)]
        random.shuffle(pics_pairs)
        result['pic_pairs'] = pics_pairs

    return jsonify(result)


@api.route('/reply/submit', methods=['POST']) # JSON
def submit_reply():
    logger.info(request.headers['X-Real-IP'])
    data = request.get_json()
    logger.debug(data)
    p_id = data['p_id']
    name = data['name']
    email = data['email']
    no = data['no']
    sex = data['sex']
    age = data['age']
    phone = data['phone']
    answers = data['answers']

    result = PsyxDB.add_reply(p_id=p_id, name=name, email=email, no=no, sex=sex, age=age, phone=phone, answers=answers)
    
    if result == -1:
        abort(STATUS.INVALID_INPUT.value, 'Invalid Input. Failed To Submit Your Reply')
    if result == -2:
        abort(STATUS.SERVER_ERROR.value, 'Server Error. Failed To Submit Your Reply')

    return 'Reply Submited.'
