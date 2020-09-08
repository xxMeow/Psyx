from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from PsyxDB import Pack, Reply
import PsyxDB

api = Flask(__name__)
CORS(api)
api.debug = True

@api.route('/pack', methods=['GET'])
def pack():
    if request.method == 'GET': # Get a pack by age and gender
        age = request.args.get('age', type=int)
        gender = request.args.get('gender', type=int)
        result = PsyxDB.GetPackName(age=age, gender=gender)
        print(result)
        return jsonify(result)
    # elif request.method == 'POST': # Add a pack
        #

@api.route('/reply', methods=['GET', 'POST'])
def reply():
    print("reply()!!")
    if request.method == 'GET': # Get all replies of the pack
        name = request.args.get('name')
        result = PsyxDB.GetAllReply(name)
        return jsonify(result)
    elif request.method == 'POST': # Add a reply
        data = request.get_json()
        name = data['name']
        r = Reply(mail=data['mail'],
                  student_no=data['studentNo'],
                  gender=data['gender'],
                  age=data['age'],
                  affiliation=data['affiliation'],
                  answer=data['answer'])
        result = { 'result' : 'Failed' }
        if r.Validation == True:
            result = PsyxDB.PostReply(name, r)
        return jsonify(result)
