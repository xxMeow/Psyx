import pymysql
import sys, os, re, json # need shutil??

class Tool():
    # Class Constants : please DONT'T change any of them!
    PACK_SIZE = 600 # == $
    AGE_MIN = 0 # >= $
    AGE_MAX = 120 # <= $
    SEX_M = 1 # == $
    SEX_F = 2 # == $
    EMAIL_LEN_MAX = 48 # < $
    NAME_LEN_MAX = 64 # < $
    PHONE_LEN = 13 # == $ (xxx-xxxx-xxxx)
    NO_LEN_MAX = 20 # only (alphabet, number)
    PACK_NAME_LEN_MAX = 16 # only (alphabet, numer, underbar)
    PACK_BASE_PATH = os.path.join(os.environ['HOME'], 'Psyx', 'packs')
    UPLOAD_PATH = os.environ['HOME']

    @classmethod
    def check_email(cls, email):
        print(' * ', sys._getframe().f_code.co_name, ': "', email, '"')
        if not isinstance(email, str):
            return False
        if len(email) >= cls.EMAIL_LEN_MAX:
            return False
        if re.match(r"^[A-Za-z0-9]+[A-Za-z0-9\.\+_-]*@[A-Za-z0-9\._-]+\.[a-zA-Z0-9]+$", email) is None:
            return False
        return True

    @classmethod
    def check_name(cls, name):
        print(' * ', sys._getframe().f_code.co_name, ': "', name, '"')
        if not isinstance(name, str):
            return False
        if len(name) >= cls.NAME_LEN_MAX:
            return False
        if re.match(r"^[가-힣]{2,}$", name) is None: # only korean characters without space, 2 characters at least
            return False
        return True

    @classmethod
    def check_phone(cls, phone):
        print(' * ', sys._getframe().f_code.co_name, ': "', phone, '"')
        if not isinstance(phone, str):
            return False
        if len(phone) != cls.PHONE_LEN:
            return False
        if re.match(r"^\d{3}-\d{4}-\d{4}$", phone) is None:
            return False
        return True

    @classmethod
    def check_sex(cls, sex):
        print(' * ', sys._getframe().f_code.co_name, ': "', sex, '"')
        if not isinstance(sex, int):
            print('\t\twrong type : sex=', sex, 'is', str(type(sex)))
            return False
        if sex != cls.SEX_F and sex != cls.SEX_M:
            return False
        return True

    @classmethod
    def check_age(cls, age):
        print(' * ', sys._getframe().f_code.co_name, ': "', age, '"')
        if not isinstance(age, int):
            return False
        if age < cls.AGE_MIN or age > cls.AGE_MAX:
            return False
        return True

    @classmethod
    def check_no(cls, no):
        print(' * ', sys._getframe().f_code.co_name, ': "', no, '"')
        if not isinstance(no, str):
            return False
        if len(no) >= cls.NO_LEN_MAX:
            return False
        if re.match(r"^[A-Za-z0-9]+$", no) is None: # only allow numbers and characters
            return False
        return True

    @classmethod
    def check_pack_name(cls, pack_name):
        print(' * ', sys._getframe().f_code.co_name, ': "', pack_name, '"')
        if not isinstance(pack_name, str):
            return False
        if len(pack_name) >= cls.PACK_NAME_LEN_MAX:
            return False
        if re.match(r"^[A-Za-z0-9_]+$", pack_name) is None: # only allow numbers and characters
            return False
        return True

    @classmethod
    def check_file_type(cls, filename):
        print(' * ', sys._getframe().f_code.co_name, ': "', filename, '"')
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # TODO: more strict?
        return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)
    
    @classmethod
    def check_file_name(cls, filename):
        # TODO: to be completed
        return True
    
    @classmethod
    def absorb_filename(cls, filename):
        return filename.split(os.sep)[-1]



def _login_as_admin():
    print(' * ',sys._getframe().f_code.co_name)
    return pymysql.connect(host='localhost',
                           user='xmx1025',
                           password='lamj810327',
                           db='psyx',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)

def _login_as_visitor():
    print(' * ',sys._getframe().f_code.co_name)
    return pymysql.connect(host='localhost',
                           user='visitor',
                           password='12345678',
                           db='psyx',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


def get_all_packs():
    print(' * ',sys._getframe().f_code.co_name)
    sql = 'SELECT p.*, r.count '\
          'FROM pack p LEFT JOIN (SELECT p_id, COUNT(*) count FROM reply GROUP BY p_id) r '\
          'ON p.p_id=r.p_id'
    # SELECT p.*, r.count FROM pack p LEFT JOIN (SELECT p_id, COUNT(*) count FROM reply GROUP BY p_id) r ON p.p_id=r.p_id

    result = []
    db = _login_as_visitor()
    with db.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    db.close()

    return result


def add_pack(sex, age_lower, age_upper, pack_name):
    print(' * ', sys._getframe().f_code.co_name, ':', sex, age_lower, age_upper, pack_name)
    sql = 'INSERT INTO pack VALUES (NULL, %s, %s, %s, %s, sysdate())'

    p_id = 0
    db = _login_as_admin()
    with db.cursor() as cursor:
        try:
            cursor.execute(sql, (sex, age_lower, age_upper, pack_name))
            db.commit()
            p_id = cursor.lastrowid
            print('\t\tnew p_id :', str(p_id))
        except:
            db.rollback()
    db.close()

    return p_id # TODO: if p_id == 0, delete all uploaded files

def delete_pack(p_id):
    print(' * ',sys._getframe().f_code.co_name, ':', p_id)
    # delete all replies of this pack
    sql1 = 'SELECT pack_name FROM pack WHERE p_id=%s'
    sql2 = 'DELETE FROM reply WHERE p_id=%s'
    sql3 = 'DELETE FROM pack WHERE p_id=%s'

    result = None
    db = _login_as_admin()
    with db.cursor() as cursor:
        if cursor.execute(sql1, (p_id)) > 0:
            result = cursor.fetchall()
        try:
            cursor.execute(sql2, (p_id))
            cursor.execute(sql3, (p_id))
            db.commit()
        except:
            db.rollback()
    db.close()

    pack_name = None
    if result != None:
        print(result)
        pack_name = result[0]['pack_name']
    return pack_name # TODO: if pack_name == None, packbase damaged. -> delete the pack?

def get_all_replies(p_id):
    print(' * ',sys._getframe().f_code.co_name, ':', p_id)
    sql = 'SELECT * FROM reply WHERE p_id=%s'

    result = []
    db = _login_as_visitor()
    with db.cursor() as cursor:
        cursor.execute(sql, (p_id))
        result = cursor.fetchall()
    db.close()

    return result

def get_pack_path(sex, age):
    print(' * ',sys._getframe().f_code.co_name, ':', sex, age)
    sql = 'SELECT p_id, pack_name FROM pack WHERE sex=%s and age_lower<=%s AND age_upper>=%s'

    result = []
    db = _login_as_visitor()
    with db.cursor() as cursor:
        cursor.execute(sql, (sex, age, age))
        result = cursor.fetchall()
    db.close()

    p_id = 0
    pack_name = None
    if result != None and len(result) == 1:
        p_id = result[0]['p_id']
        pack_name = result[0]['pack_name']
    return (p_id, pack_name)

def add_reply(p_id, name, email, no, sex, age, phone, answers):
    print(' * ',sys._getframe().f_code.co_name, ':', p_id, name, email, no, sex, age, phone, '[answers]')
    result = False

    print(' * Testing args..')
    if (Tool.check_name(name) and Tool.check_email(email) and Tool.check_sex(sex) and Tool.check_age(age)
        and Tool.check_no(no) and Tool.check_phone(phone)):
        print(' * Tested : len(answers) =', len(answers))
        # TODO: check age and sex with the pack's condition?
        # BUT: if p_id doesn't exist, the following insertion will abort anyway
        if len(answers) > 0: # == Tool.PACK_SIZE: # TODO: check the number of answers
            answers_str = json.dumps(answers)
            print('\t', answers_str)

            # TODO: is it ok to insert JSON data like this?
            sql = 'INSERT INTO reply VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, sysdate(), %s)'
            db = _login_as_visitor()
            with db.cursor() as cursor:
                try:
                    cursor.execute(sql, (p_id, name, email, no, sex, age, phone, answers_str))
                    db.commit()
                    result = True
                except:
                    db.rollback()
            db.close()

    return result