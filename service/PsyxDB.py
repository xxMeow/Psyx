import pymysql
import os, re, json
import configparser

# set config
config = configparser.ConfigParser()
config.read('../config/psyx.ini')


class Tool():
    # Class Constants : please DONT'T change any of them!
    PACK_SIZE = 300 # == $
    AGE_MIN = 0 # >= $
    AGE_MAX = 120 # <= $
    SEX_M = 1 # == $
    SEX_F = 2 # == $
    EMAIL_LEN_MAX = 48 # < $
    NAME_LEN_MAX = 64 # < $
    PHONE_LEN = 13 # == $
    NO_LEN_MAX = 20 # < $
    PACK_NAME_LEN_MAX = 16 # < $
    PROJ_PATH = os.path.join(os.environ['HOME'], config['directory']['proj_dir'])
    PACKBASE_PATH = os.path.join(PROJ_PATH, config['directory']['packbase_dir'])
    LOGBASE_PATH = os.path.join(PROJ_PATH, config['directory']['logbase_dir'])
    PACKBASE_LOC = config['location']['packbase_loc']

    @classmethod
    def check_email(cls, email):
        if not isinstance(email, str):
            return False
        if len(email) >= cls.EMAIL_LEN_MAX:
            return False
        if re.match(r'^[A-Za-z0-9]+[A-Za-z0-9\.\+_-]*@[A-Za-z0-9\._-]+\.[a-zA-Z0-9]+$', email) is None:
            return False
        return True

    @classmethod
    def check_name(cls, name):
        if not isinstance(name, str):
            return False
        if len(name) >= cls.NAME_LEN_MAX:
            return False
        if re.match(r'^[가-힣]{2,}$', name) is None:
            return False
        return True

    @classmethod
    def check_phone(cls, phone):
        if not isinstance(phone, str):
            return False
        if len(phone) != cls.PHONE_LEN:
            return False
        if re.match(r'^\d{3}-\d{4}-\d{4}$', phone) is None:
            return False
        return True

    @classmethod
    def check_sex(cls, sex):
        if not isinstance(sex, int):
            return False
        if sex != cls.SEX_F and sex != cls.SEX_M:
            return False
        return True

    @classmethod
    def check_age(cls, age):
        if not isinstance(age, int):
            return False
        if age < cls.AGE_MIN or age > cls.AGE_MAX:
            return False
        return True

    @classmethod
    def check_no(cls, no):
        if not isinstance(no, str):
            return False
        if len(no) >= cls.NO_LEN_MAX:
            return False
        if re.match(r'^[A-Za-z0-9]+$', no) is None:
            return False
        return True

    @classmethod
    def check_pack_name(cls, pack_name):
        if not isinstance(pack_name, str):
            return False
        if len(pack_name) >= cls.PACK_NAME_LEN_MAX:
            return False
        if re.match(r'^[a-z][a-z0-9_]*$', pack_name) is None:
            return False
        return True

    @classmethod
    def check_file_name(cls, filename):
        if len(filename) < 13:
            return False
        suffix = re.search(r'00[0-3][0-9]{2}_(ori|inv)\.(jpg|JPG)$', filename[-13:])
        if suffix is None:
            return False
        order = int(suffix.group(0)[2 : 5])
        if order <= 0 or order > 300:
            return False
        return True

    @classmethod
    def absorb_filename(cls, filepath):
        return filepath.split(os.sep)[-1]


def _login_as_admin():
    return pymysql.connect(host='localhost',
                           user=config['database']['admin_name'],
                           password=config['database']['admin_pw'],
                           db=config['database']['db_name'],
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)

def _login_as_visitor():
    return pymysql.connect(host='localhost',
                           user=config['database']['visitor_name'],
                           password=config['database']['visitor_pw'],
                           db=config['database']['db_name'],
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


def get_all_packs():
    sql = 'SELECT p.*, r.count '\
          'FROM pack p LEFT JOIN (SELECT p_id, COUNT(*) count FROM reply GROUP BY p_id) r '\
          'ON p.p_id=r.p_id'
    # SELECT p.*, r.count FROM pack p LEFT JOIN (SELECT p_id, COUNT(*) count FROM reply GROUP BY p_id) r ON p.p_id=r.p_id

    result = ()
    db = _login_as_visitor()
    with db.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    db.close()

    return result

def add_pack(sex, age_min, age_max, pack_name):
    p_id = 0
    sql = 'SELECT * FROM pack WHERE sex=%s AND '\
          '((age_min <= %s AND age_max >= %s) OR (age_min <= %s AND age_max >= %s) '\
          'OR (age_min <= %s AND age_max >= %s) OR (age_min >= %s AND age_max <= %s))'
    result = ()
    db = _login_as_visitor()
    with db.cursor() as cursor:
        cursor.execute(sql, (sex, age_min, age_min, age_max, age_max, age_min, age_max, age_min, age_max))
        result = cursor.fetchall()
    db.close()
    if len(result) > 0:
        return p_id # conditions overlapped

    p_id = -1
    sql = 'INSERT INTO pack VALUES (NULL, %s, %s, %s, %s, sysdate())'
    db = _login_as_admin()
    with db.cursor() as cursor:
        try:
            cursor.execute(sql, (sex, age_min, age_max, pack_name))
            db.commit()
            p_id = cursor.lastrowid
        except:
            db.rollback()
    db.close()

    return p_id

def delete_pack(p_id):
    # delete all replies of this pack
    sql1 = 'SELECT pack_name FROM pack WHERE p_id=%s'
    sql2 = 'DELETE FROM reply WHERE p_id=%s'
    sql3 = 'DELETE FROM pack WHERE p_id=%s'

    result = ()
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
    if len(result) > 0:
        pack_name = result[0]['pack_name']
    return pack_name

def get_pack_info(p_id):
    sql = 'SELECT * FROM pack WHERE p_id=%s'

    result = ()
    db = _login_as_visitor()
    with db.cursor() as cursor:
        cursor.execute(sql, (p_id))
        result = cursor.fetchall()
    db.close()

    return result

def get_all_replies(p_id):
    sql = 'SELECT * FROM reply WHERE p_id=%s'

    result = ()
    db = _login_as_visitor()
    with db.cursor() as cursor:
        cursor.execute(sql, (p_id))
        result = cursor.fetchall()
    db.close()

    return result

def get_pack_path(sex, age):
    sql = 'SELECT p_id, pack_name FROM pack WHERE sex=%s AND age_min<=%s AND age_max>=%s'

    result = ()
    db = _login_as_visitor()
    with db.cursor() as cursor:
        cursor.execute(sql, (sex, age, age))
        result = cursor.fetchall()
    db.close()

    p_id = 0
    pack_name = None
    if len(result) == 1:
        p_id = result[0]['p_id']
        pack_name = result[0]['pack_name']
    return (p_id, pack_name)

def add_reply(p_id, name, email, no, sex, age, phone, answers):
    result = -2

    if (Tool.check_name(name) and Tool.check_email(email) and Tool.check_sex(sex) and Tool.check_age(age)
        and Tool.check_no(no) and Tool.check_phone(phone) and len(answers) == Tool.PACK_SIZE):
        answers_str = json.dumps(answers)
        sql = 'INSERT INTO reply VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, sysdate(), %s)'
        db = _login_as_visitor()
        with db.cursor() as cursor:
            try:
                cursor.execute(sql, (p_id, name, email, no, sex, age, phone, answers_str))
                db.commit()
                result = 0
            except:
                db.rollback()
        db.close()
    else :
        result = -1

    return result