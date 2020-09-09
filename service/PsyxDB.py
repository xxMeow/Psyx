import pymysql
import os, re, shutil, json

class Tool():
    # Class Constants : please DONT'T change any of them!
    PACK_SIZE = 300
    AGE_MIN = 0
    AGE_MAX = 100
    GENDER_F = 1
    GENDER_M = 2
    MAIL_LEN_MAX = 48
    STUDENT_NO_LEN_MAX = 16
    AFFILIATION_LEN_MAX = 48
    PACK_NAME_LEN_MAX = 32
    PACK_BASE_PATH = os.path.join(os.environ['HOME'], 'Psyx', 'packbase')
    UPLOAD_PATH = os.environ['HOME']

    @classmethod
    def check_mail(cls, mail):
        if not isinstance(mail, str):
            return False
        mail = mail.strip() # remove the leading and tailing spaces
        if len(mail) >= cls.MAIL_LEN_MAX:
            return False
        if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", mail) is not None:
            return True
        return False

    @classmethod
    def check_gender(cls, gender):
        if not isinstance(gender, int):
            return False
        if gender == cls.GENDER_F or gender == cls.GENDER_M:
            return True
        return False

    @classmethod
    def check_age(cls, age):
        if not isinstance(age, int):
            return False
        if age >= cls.AGE_MIN and age <= cls.AGE_MAX:
            return True
        return False

    @classmethod
    def check_student_no(cls, student_no):
        if not isinstance(student_no, str):
            return False
        student_no = student_no.strip() # remove the leading and tailing spaces
        if len(student_no) >= cls.STUDENT_NO_LEN_MAX:
            return False
        if re.match(r"^[A-Za-z0-9]$", student_no) is not None: # only allow numbers and characters
            return True
        return False

    @classmethod
    def check_affiliation(cls, affiliation):
        if not isinstance(affiliation, str):
            return False
        affiliation = affiliation.strip() # remove the leading and tailing spaces
        if len(affiliation) < cls.AFFILIATION_LEN_MAX:
            return True
        return False

    @classmethod
    def _check_pack_name(cls, pack_name):
        if not isinstance(pack_name, str):
            return False
        pack_name = pack_name.strip() # remove the leading and tailing spaces
        if len(pack_name) >= cls.PACK_NAME_LEN_MAX:
            return False
        if re.match(r"^[A-Za-z0-9]$", pack_name) is not None: # only allow numbers and characters
            return True
        return False

    @classmethod
    def move_pack_in(cls, pack_name): # used when adding a new pack
        if cls._check_pack_name(pack_name) != True:
            return False

        src_path = os.path.join(cls.UPLOAD_PATH, pack_name)
        dst_path = os.path.join(cls.PACK_BASE_PATH, pack_name)
        if not os.path.exists(src_path) or os.path.isdir(src_path) == False:
            return False
        if os.path.exists(dst_path):
            return False

        # check the uploaded folder
        pic_count = 0
        for i in os.listdir(src_path):
            if os.path.isdir(i) == True:
                return False
            else:
                pic_count += 1
        if pic_count == cls.PACK_SIZE:
            # TODO: file names check?
            shutil.copytree(src_path, dst_path)
            shutil.rmtree(src_path)
            return True

        shutil.rmtree(src_path)
        return False

    @classmethod
    def move_pack_out(cls, pack_name): # used when removing a pack
        if cls._check_pack_name(pack_name) != True: # TODO: necessery?
            return False

        pack_path = os.path.join(cls.PACK_BASE_PATH, pack_name)
        if os.path.exists(pack_path) and os.path.isdir(pack_path) == True:
            shutil.rmtree(pack_path)
            return True
        return False


def _login_as_admin():
    return pymysql.connect(host='localhost',
                           user='xmx1025',
                           password='lamj810327',
                           db='psyx',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)

def _login_as_visitor():
    return pymysql.connect(host='localhost',
                           user='visitor',
                           password='12345678',
                           db='psyx',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


def get_all_packs():
    sql = 'SELECT p.*, r.count \
        FROM pack p \
        LEFT JOIN (SELECT p_id, COUNT(*) count FROM reply GROUP BY p_id) r \
        ON p.p_id=r.p_id'
    print('get_all_packs()')
    print('\t' + sql)
 
    result = []
    db = _login_as_visitor()
    with db.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    db.close()

    return result


def add_pack(gender, age_lower, age_upper, pack_name):
    sql = 'INSERT INTO pack VALUES (NULL, {}, {}, {}, {}, sysdate())' \
        .format(gender, age_lower, age_upper, pack_name)
    print('add_pack(gender={}, age_l={}, age_h={}, name={})'.format(gender, age_lower, age_upper, pack_name))
    print('\t' + sql)

    p_id = 0
    db = _login_as_admin()
    try:
        with db.cursor() as cursor:
            cursor.execute(sql)
        p_id = db.insert_id()
        db.commit()
    except:
        db.rollback()
        print('[ERROR] : add_pack() Failed.')
    db.close()
    return p_id

def delete_pack(p_id):
    # delete all replies of this pack
    sql1 = 'DELETE FROM reply WHERE p_id={}'.format(p_id)
    sql2 = 'SELECT name FROM pack WHERE p_id={}'.format(p_id)
    sql3 = 'DELETE FROM pack WHERE p_id={}'.format(p_id)
    print('delete_pack(p_id={})'.format(p_id))
    print('\t' + sql1)
    print('\t' + sql2)
    print('\t' + sql3)

    result = []
    db = _login_as_admin()
    try:
        with db.cursor as cursor:
            cursor.execute(sql1)
            cursor.execute(sql2)
            result = cursor.fetchall()
            cursor.execute(sql3)
        db.commit()
    except:
        result = None
        db.rollback()
    db.close()

    pack_name = None
    if result != None:
        pack_name = result[0]['name']
    return pack_name

def get_all_replies(p_id):
    sql = 'SELECT * FROM reply WHERE p_id={}' \
        .format(p_id)
    print('get_all_replies(p_id={})'.format(p_id))
    print('\t' + sql)

    result = []
    db = _login_as_visitor()
    with db.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    db.close()

    return result

def get_pack_path(gender, age):
    sql = 'SELECT p_id, pack_name FROM pack WHERE gender={} and age_lower<={} AND age_upper>={}' \
        .format(gender, age, age)
    print('get_pack_path(gender={}, age={})'.format(gender, age))
    print('\t' + sql)

    result = []
    db = _login_as_visitor()
    with db.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    db.close()

    p_id = 0
    pack_path = None
    if result != None and len(result) == 1:
        p_id = result[0]['p_id']
        pack_path = os.path.join(Tool.PACK_BASE_PATH, result[0]['pack_name'])
    return (p_id, pack_path)

def add_reply(p_id, mail, student_no, gender, age, affiliation, answers):
    result = False

    if (Tool.check_mail(mail) and Tool.check_gender(gender) and Tool.check_age(age)
        and Tool.check_student_no(student_no) and Tool.check_affiliation(affiliation)) == True:
        # TODO: check age and gender with the pack's condition?
        # BUT: if p_id doesn't exist, the following insertion will abort anyway
        if len(answers) == Tool.PACK_SIZE:
            # TODO: is it ok to insert JSON data like this?
            sql = 'INSERT INTO reply VALUES (NULL, {}, {}, {}, {}, {}, {}, sysdate(), {})' \
                .format(p_id, mail, student_no, gender, age, affiliation, answers)
            db = _login_as_visitor()
            try:
                with db.cursor() as cursor:
                    cursor.execute(sql)
                db.commit()
                result = True
            except:
                db.rollback()
                print('[ERROR] : PostReply() Failed.')
            db.close()
    return result
