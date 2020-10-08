from flask import Flask, request, jsonify, abort
import PsyxDB
from PsyxDB import Tool
import os, shutil, random, json, re
from werkzeug.utils import secure_filename
from enum import Enum, unique
import logging
from logging.handlers import TimedRotatingFileHandler

# ----------------------------------------------------------------------------
# Settings
#

@unique
class STATUS(Enum):
    CLIENT_ERR = 400 # STATUS.CLIENT_ERR.value
    SERVICE_ERR = 500 # STATUS.SERVICE_ERR.value

api = Flask(__name__)

# set logger
log_name = 'api'
log_format = '[%(asctime)s * %(levelname)s]\t%(lineno)d \t%(funcName)s: %(message)s'
log_path = os.path.join(Tool.LOGBASE_PATH, log_name)
logger = logging.getLogger(log_name)
logger.setLevel(logging.INFO) # DEBUG < INFO < WARNING < ERROR < CRITICAL
# make one 1 log file every midnight, keep for 14 days
file_handler = TimedRotatingFileHandler(filename=log_path, when='MIDNIGHT', interval=1, backupCount=14)
file_handler.suffix = '%Y%m%d.log'
file_handler.extMatch = re.compile(r'^\d{8}.log$')
file_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(file_handler)


# ----------------------------------------------------------------------------
# Error Handlers
#

@api.errorhandler(STATUS.CLIENT_ERR.value)
def handle_client_err(msg):
    logger.warning(request.headers['X-Real-IP'])
    logger.warning('> %s' % msg)
    return msg, STATUS.CLIENT_ERR.value


@api.errorhandler(STATUS.SERVICE_ERR.value)
def handle_service_err(msg):
    logger.error(request.headers['X-Real-IP'])
    logger.error('> %s' % msg)
    result = '< 서버 오류 : 시스템 관리자와 연락하세요 > %s' % msg
    return result, STATUS.SERVICE_ERR.value


# ----------------------------------------------------------------------------
# API: /admin/
#

@api.route('/admin/list', methods=['GET'])
def list_packs():
    logger.info(request.headers['X-Real-IP'])

    result = PsyxDB.get_all_packs()
    for each in result: # the count will be null if that set hasn't received any replies
        each['date'] = str(each['date'])
        if each['count'] is None:
            each['count'] = 0

    return jsonify(result)


@api.route('/admin/create', methods=['POST']) # FORM
def create_pack():
    logger.info(request.headers['X-Real-IP'])

    # check if the post request has the file part
    if 'file' not in request.files:
        abort(STATUS.CLIENT_ERR.value, '올린 폴더에 파일이 없습니다.')

    # read args and validation
    pack_name = request.form.get('pack_name', type=str)
    if not Tool.check_pack_name(pack_name):
        abort(STATUS.CLIENT_ERR.value, '잘못된 세트명입니다.')
    age_min = request.form.get('age_min', type=int)
    age_max = request.form.get('age_max', type=int)
    if not Tool.check_age(age_min) or not Tool.check_age(age_max) or age_min > age_max:
        abort(STATUS.CLIENT_ERR.value, '잘못된 나이 범위입니다.')
    sex = int(request.form.get('sex', type=str))
    if Tool.check_sex(sex) == False:
        abort(STATUS.SERVICE_ERR.value, 'Invalid Sex.')

    # check if packbase exists
    if not os.path.exists(Tool.PACKBASE_PATH):
        abort(STATUS.SERVICE_ERR.value, 'Packbase Damaged!')
    # check if there's any folder with the same name
    dst_path = os.path.join(Tool.PACKBASE_PATH, pack_name)
    if os.path.exists(dst_path):
        abort(STATUS.CLIENT_ERR.value, '이미 존재한 세트입니다.')
    
    # filter uploaded files
    files = [] # [(f0, n0), (f1, n1), (f2, n2), ...], f for file, n for filename
    for f in request.files.getlist('file'):
        if not f or f.filename == '':
            # if user does not select file, browser also submit an empty part without filename
            abort(STATUS.CLIENT_ERR.value, '선택된 파일이 없습니다.')
        n = secure_filename(Tool.absorb_filename(f.filename))
        if Tool.check_file_name(n): # check for both file's type and name format
            files.append((f, n))
        else:
            logger.info('- filtered file %s' % n)

    # make pack folder and save files
    if (len(files) == Tool.PACK_SIZE * 2):
        logger.info('- making pack %s..' % dst_path)
        try:
            os.makedirs(dst_path)
            for f, n in files: # f for file, n for filename
                try:
                    f.save(os.path.join(dst_path, n))
                except:
                    shutil.rmtree(dst_path)
                    abort(STATUS.SERVICE_ERR.value, 'Failed to Save Files.')
        except:
            abort(STATUS.SERVICE_ERR.value, 'Failed to Make Folder.')
    else:
        abort(STATUS.CLIENT_ERR.value, '잘못된 세트 사이즈입니다.')
    
    logger.info('> pack_name=%s age_min=%s age_max=%s sex=%s dst_path=%s' % (pack_name, age_min, age_max, sex, dst_path))

    # add to db
    p_id = PsyxDB.add_pack(sex=sex, age_min=age_min, age_max=age_max, pack_name=pack_name)
    if p_id == 0:
        shutil.rmtree(dst_path) # delete folder
        abort(STATUS.CLIENT_ERR.value, '기존 세트와 조건이 중복되었습니다.')
    if p_id == -1:
        shutil.rmtree(dst_path) # delete folder
        abort(STATUS.SERVICE_ERR.value, 'Failed to Add Pack to DB.')
    return '세트 %s 추가되었습니다.' % p_id


@api.route('/admin/remove', methods=['GET']) # id
def remove_pack():
    logger.info(request.headers['X-Real-IP'])

    # delete pack from db and return pack_name
    p_id = request.args.get('id', type=int)
    pack_name = PsyxDB.delete_pack(p_id)

    logger.info('> p_id=%s pack_name=%s' % (p_id, pack_name))

    # check if pack deleted from db successfully
    if pack_name is not None:
        pack_path = os.path.join(Tool.PACKBASE_PATH, pack_name)
        logger.info('- removing pack %s..' % pack_path)
        try:
            shutil.rmtree(pack_path)
        except:
            abort(STATUS.SERVICE_ERR.value, 'Packbase Damaged!')
    else:
        abort(STATUS.SERVICE_ERR.value, 'Unknown Pack %s.' % p_id)

    return '세트 %s 삭제되었습니다.' % p_id


@api.route('/admin/download', methods=['GET']) # id
def download_pack():
    logger.info(request.headers['X-Real-IP'])

    p_id = request.args.get('id', type=int)
    pack_info = PsyxDB.get_pack_info(p_id)

    logger.info('> p_id=%s' % (p_id))

    if len(pack_info) == 0:
        abort(STATUS.SERVICE_ERR.value, 'Unknown Pack %s.' % p_id)
    result = pack_info[0] # dict
    replies = PsyxDB.get_all_replies(p_id) # a list of dictionaries (each dic is a record in db)
    for r in replies:
        r['date'] = str(r['date'])
        r['answers'] = json.loads(r['answers']) # the answers data in db is jsonstring
    result['replies'] = replies

    return jsonify(result)


# ----------------------------------------------------------------------------
# API: /reply/
#

@api.route('/reply/start', methods=['POST']) # FORM
def start_reply():
    logger.info(request.headers['X-Real-IP'])

    # get inputs
    data = request.get_json()
    logger.debug(data)
    name = data['name'].strip() # remove the leading and tailing space(s)
    email = data['email']
    no = data['no']
    sex = data['sex']
    age = data['age']
    phone = data['phone']
    logger.info('> name=%s email=%s no=%s sex=%s age=%s phone=%s' % (name, email, no, sex, age, phone))

    # validate inputs
    if Tool.check_name(name) != True:
        abort(STATUS.CLIENT_ERR.value, '이름을 다시 확인해주세요.')
    if Tool.check_email(email) != True:
        abort(STATUS.CLIENT_ERR.value, '이메일 주소를 다시 확인해주세요.')
    if Tool.check_sex(sex) != True:
        abort(STATUS.SERVICE_ERR.value, 'Invalid Sex.')
    if Tool.check_age(age) != True:
        abort(STATUS.SERVICE_ERR.value, 'Invalid Age.')
    if Tool.check_no(no) != True:
        abort(STATUS.CLIENT_ERR.value, 'ID를 다시 확인해주세요.')
    if Tool.check_phone(phone) != True:
        abort(STATUS.CLIENT_ERR.value, '전화 번호를 다시 확인해주세요.')

    # validation passed, get pack info from db
    p_id, pack_name = PsyxDB.get_pack_path(sex=sex, age=age)
    if p_id == 0 or pack_name is None:
        abort(STATUS.CLIENT_ERR.value, '입력하신 조건으로 참여할 수 있는 세트가 없습니다.')
    else:
        result = {}
        result['p_id'] = p_id
        result['pack_path'] = Tool.PACKBASE_LOC + pack_name
        pics = []
        for i in os.listdir(os.path.join(Tool.PACKBASE_PATH, pack_name)):
            pics.append(i)
        pics.sort()
        pics_pairs = [pics[i:i+2] for i in range(0, len(pics), 2)] # ATTENTION! by alphabet order, the ori and inv are inverted
        random.shuffle(pics_pairs)
        result['pic_pairs'] = pics_pairs

    return jsonify(result)


@api.route('/reply/submit', methods=['POST']) # JSON
def submit_reply():
    logger.info(request.headers['X-Real-IP'])

    # get inputs
    data = request.get_json()
    logger.debug(data)
    p_id = data['p_id']
    name = data['name'].strip() # remove the leading and tailing space(s)
    email = data['email']
    no = data['no']
    sex = data['sex']
    age = data['age']
    phone = data['phone']
    answers = data['answers']

    logger.info('> p_id=%s name=%s email=%s no=%s sex=%s age=%s phone=%s' % (p_id, name, email, no, sex, age, phone))

    # the validation will be done inside PsyxDB.add_reply()
    result = PsyxDB.add_reply(p_id=p_id, name=name, email=email, no=no, sex=sex, age=age, phone=phone, answers=answers)
    
    if result == -1:
        abort(STATUS.SERVICE_ERR.value, 'Invalid Input. Failed to Submit Reply to Pack %s.' % p_id)
    if result == -2:
        abort(STATUS.SERVICE_ERR.value, 'Server Error. Failed to Submit Reply to Pack %s.' % p_id)

    return '수고하셨습니다. 성공적으로 제출되었습니다.'
