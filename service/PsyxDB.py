import pymysql
import os.path
import json

PACK_PATH = "/home/xmx1025/Psyx/pack/"

def loginAsAdmin():
    return pymysql.connect(host='localhost',
                           user='xmx1025',
                           password='lamj810327',
                           db='psyx',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)

def loginAsVisitor():
    return pymysql.connect(host='localhost',
                           user='visitor',
                           password='12345678',
                           db='psyx',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)

class Pack():
    def __init__(self, gender, age_low, age_high, name, p_id=0, date=0):
        self.p_id = p_id
        self.gender = gender
        self.age_low = age_low
        self.age_high = age_high
        self.name = name
        self.date = date

    @staticmethod
    def Validation(p):
        flag = False
        if isinstance(p.gender, int) and isinstance(p.age_low, int) and isinstance(p.age_high, int):
            if p.gender >= 0 and p.gender < 3 and p.age_low >= 0 and p.age_high <= 150 and p.age_low < p.age_high:
                if isinstance(p.name, str) and os.path.isdir(PACK_PATH + p.name):
                    flag = True
        return flag

    def __str__(self):
        contents = '[{}]th pack:\n\tAge[{}, {})\tGender: {}\n\tLocation: {}\n\tDate: {}'\
            .format(self.p_id, self.age_low, self.age_high, self.gender, PACK_PATH+self.name, self.date)
        return contents

class Reply():
    def __init__(self, mail, student_no, gender, age, affiliation, answer, r_id=0, p_id=0, date=0):
        self.r_id = r_id
        self.p_id = p_id
        self.mail = mail
        self.student_no = student_no
        self.gender = gender
        self.age = age
        self.affiliation=affiliation
        self.answer = answer
        self.date = date
    
    @staticmethod
    def Validation(r):
        flag = False
        if isinstance(r.mail, str) and isinstance(r.student_no, str) and isinstance(r.gender, int):
            if r.gender >= 0 and r.gender < 3 and isinstance(r.age, int):
                if isinstance(r.affiliation, str) and isinstance(r.answer, str):
                    try:
                        r.answer = json.loads(r.answer)
                        flag = True
                    except:
                        flag = False
        return flag

    def __str__(self):
        contents = '[{}]th reply:\n\tMail: {}\n\tStudentNo: {}\n\tGender: {}'\
            .format(self.r_id, self.mail, self.student_no, self.gender)
        return contents

def GetPackName(age, gender): # Post only gender+age to server to get image path
    # Select (age, gender) in DB
    sql = "SELECT p_id, name FROM pack WHERE gender={} and age_low<={} AND age_high>={}"\
        .format(gender, age, age)
    result = []

    db = loginAsVisitor()
    with db.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    db.close()
    print("**** " + str(result))
    result.append({'p_id': 0, 'name': 'None'})

    return result[0]

def GetAllReply(name):
    sql = "SELECT pack.p_id, reply.*\
        FROM pack INNER JOIN reply\
        WHERE pack.name={} AND pack.p_id=reply.p_id"\
        .format(name)
    result = {}

    db = loginAsVisitor()
    with db.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    db.close()

    return result

def PostReply(name, r): # Post the whole reply
    result = { 'result' : 'Failed' }

    sql = 'INSERT INTO reply VALUES (NULL, %s, %s, %s, %s, sysdate(), %s)'
    db = loginAsVisitor()
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (r.mail, r.student_no, r.gender, r.affiliation, r.answer))
        db.commit()
        result['result'] = 'Succeed'
    except:
        db.rollback()
        result = -1
        print('[ERROR] : PostReply() Failed.')
    db.close()
    
    return result
