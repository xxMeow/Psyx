from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import PsyxDB
from PsyxDB import Tool
import sys

api = Flask(__name__)
CORS(api)
api.debug = True

@api.route('/admin/list', methods=['GET']) # FIXME:
def list_packs():
    print(' * ',sys._getframe().f_code.co_name)
    result = {}
    packs = PsyxDB.get_all_packs()
    result['pack_num'] = len(packs)
    result['pack_list'] = packs
    return jsonify(result)


@api.route('/admin/create', methods=['POST']) # FORM
def create_pack():
    print(' * ',sys._getframe().f_code.co_name)
    # get inputs from form
    gender = request.form.get('gender', type=int)
    age_lower = request.form.get('age_lower', type=int)
    age_upper = request.form.get('age_upper', type=int)
    pack_name = request.form.get('pack_name', type=str)
    # make result
    result = {
        'result' : 'failed'
    }
    # mv new pack in
    if Tool.move_pack_in(pack_name) == True:
        # add to DB
        p_id = PsyxDB.add_pack(gender=gender, age_lower=age_lower, age_upper=age_upper, pack_name=pack_name)
        if p_id != 0:
            result['result'] = 'succeed'
            result['p_id'] = p_id
        else:
            result['message'] = 'DB Operation Failed'
    else:
            result['message'] = 'Invalid Folder'
    return jsonify(result)


@api.route('/admin/remove', methods=['GET']) # id
def remove_pack():
    print(' * ',sys._getframe().f_code.co_name)
    # mv Pack Folder
    p_id = request.args.get('id', type=int)
    result = {
        'result' : 'failed'
    }
    pack_name = PsyxDB.delete_pack(p_id)
    if pack_name != None:
        if Tool.move_pack_out(pack_name) == True:
            result['result'] = 'succeed'
        else:
            result['message'] = 'Can not remove this pack from base'
    else:
        result['message'] = 'Can not delete this pack from DB'

    return jsonify(result)


@api.route('/admin/download', methods=['GET']) # id FIXME:
def download_pack():
    print(' * ',sys._getframe().f_code.co_name)
    p_id = request.args.get('id', type=int)
    result = PsyxDB.get_all_replies(p_id)
    if result == None: # TODO: make csv and start downloading
        result = {
            'result' : 'failed',
            'message' : 'No Replies Yet'
        }
    return jsonify(result)


@api.route('/reply/start', methods=['POST']) # FORM
def start_reply():
    print(' * ',sys._getframe().f_code.co_name)
    # get inputs from form
    data = request.get_json()

    mail = data['mail']
    student_no = data['student_no']
    gender = data['gender']
    age = data['age']
    affiliation = data['affiliation']

    # check inputs
    result = {
        'result' : 'failed'
    }
    if Tool.check_mail(mail) != True:
        result['message'] = str(mail) + 'Invalid Mail Address'
    if Tool.check_gender(gender) != True:
        result['message'] = str(gender) + 'Invalid Gender'
        return jsonify(result)
    if Tool.check_age(age) != True:
        result['message'] = str(age) + 'Invalid Age'
        return jsonify(result)
    if Tool.check_student_no(student_no) != True:
        result['message'] = str(student_no) + 'Invalid Student ID'
        return jsonify(result)
    if Tool.check_affiliation(affiliation) != True:
        result['message'] = str(affiliation) + 'Invalid Affiliation'
        return jsonify(result)

    # get pack path
    p_id, pack_path = PsyxDB.get_pack_path(gender=gender, age=age)
    if p_id == 0 or pack_path == None:
        result['message'] = 'None Suitable Pack'
    else:
        result['result'] = 'succeed'
        result['p_id'] = p_id
        result['pack_path'] = pack_path

    return jsonify(result)


@api.route('/reply/submit', methods=['POST']) # JSON
def submit_reply():
    print(' * ',sys._getframe().f_code.co_name)
    data = request.get_json() # TODO: force=True?

    p_id = data['p_id']
    mail = data['mail']
    student_no = data['student_no']
    gender = data['gender']
    age = data['age']
    affiliation = data['affiliation']
    answers = data['answers']

    result = {
        'result' : 'failed'
    }
    if PsyxDB.add_reply(p_id=p_id, mail=mail, student_no=student_no, gender=gender,
                        age=age, affiliation=affiliation, answers=answers) == True:
        result['result'] = 'succeed'

    return jsonify(result)
