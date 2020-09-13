import pymysql
import sys, os, re, json # need shutil??

class Tool():
    # Class Constants : please DONT'T change any of them!
    PACK_SIZE = 10
    AGE_MIN = 0
    AGE_MAX = 120
    SEX_F = 1
    SEX_M = 2
    EMAIL_LEN_MAX = 48
    NAME_LEN_MAX = 64
    PHONE_LEN = 13 # number + 2 (xxx-xxxx-xxxx)
    NO_LEN_MAX = 16
    PACK_NAME_LEN_MAX = 32
    PACK_BASE_PATH = os.path.join(os.environ['HOME'], 'Psyx', 'packs')
    UPLOAD_PATH = os.environ['HOME']

    @classmethod
    def check_email(cls, email):
        print(' * ',sys._getframe().f_code.co_name)
        if not isinstance(email, str):
            return False
        email = email.strip() # remove the leading and tailing spaces
        if len(email) >= cls.EMAIL_LEN_MAX:
            return False
        if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email) is not None:
            return True
        return False

    @classmethod
    def check_name(cls, name):
        print(' * ',sys._getframe().f_code.co_name)
        if not isinstance(name, str):
            return False
        name = name.strip() # remove the leading and tailing spaces
        if len(name) >= cls.NAME_LEN_MAX:
            return False
        if re.match(r"^[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]*$", name) is not None:
            return True
        return False


    @classmethod
    def check_phone(cls, phone):
        print(' * ',sys._getframe().f_code.co_name)
        if not isinstance(phone, str):
            return False
        phone = phone.strip() # remove the leading and tailing spaces
        if len(phone) != cls.PHONE_LEN:
            return False
        if re.match(r"^\d{3}-\d{4}-\d{4}$", phone) is not None:
            return True
        return False


    @classmethod
    def check_sex(cls, sex):
        print(' * ',sys._getframe().f_code.co_name)
        if not isinstance(sex, int):
            print('\t\tsex=', sex, ' is', str(type(sex)))
            return False
        if sex == cls.SEX_F or sex == cls.SEX_M:
            return True
        return False

    @classmethod
    def check_age(cls, age):
        print(' * ',sys._getframe().f_code.co_name)
        if not isinstance(age, int):
            return False
        if age >= cls.AGE_MIN and age <= cls.AGE_MAX:
            return True
        return False

    @classmethod
    def check_no(cls, no):
        print(' * ',sys._getframe().f_code.co_name)
        if not isinstance(no, str):
            return False
        no = no.strip() # remove the leading and tailing spaces
        if len(no) >= cls.NO_LEN_MAX:
            return False
        if re.match(r"^[A-Za-z0-9]*$", no) is not None: # only allow numbers and characters
            return True
        return False


    @classmethod
    def _check_pack_name(cls, pack_name):
        print(' * ',sys._getframe().f_code.co_name)
        if not isinstance(pack_name, str):
            return False
        pack_name = pack_name.strip() # remove the leading and tailing spaces
        if len(pack_name) >= cls.PACK_NAME_LEN_MAX:
            return False
        if re.match(r"^[A-Za-z0-9]*$", pack_name) is not None: # only allow numbers and characters
            return True
        return False

    # @classmethod
    # def move_pack_in(cls, pack_name): # used when adding a new pack
    #     print(' * ',sys._getframe().f_code.co_name)
    #     if cls._check_pack_name(pack_name) != True:
    #         return False

    #     src_path = os.path.join(cls.UPLOAD_PATH, pack_name)
    #     dst_path = os.path.join(cls.PACK_BASE_PATH, pack_name)
    #     print('\tMove Pack From:')
    #     print('\t\t' + src_path + ' ->')
    #     print('\t\t' + dst_path)
    #     if not os.path.exists(src_path) or os.path.isdir(src_path) == False:
    #         return False
    #     if os.path.exists(dst_path):
    #         return False

    #     # check the uploaded folder
    #     pic_count = 0
    #     for i in os.listdir(src_path):
    #         if os.path.isdir(i) == True:
    #             return False
    #         else:
    #             pic_count += 1
    #     print('\t\tpic_count :', str(pic_count))
    #     if pic_count == cls.PACK_SIZE:
    #         # TODO: file names check?
    #         shutil.copytree(src_path, dst_path)
    #         shutil.rmtree(src_path)
    #         return True

    #     shutil.rmtree(src_path)
    #     return False

    # @classmethod
    # def move_pack_out(cls, pack_name): # used when removing a pack
    #     print(' * ',sys._getframe().f_code.co_name)
        
    #     pack_path = os.path.join(cls.PACK_BASE_PATH, pack_name)
    #     print('\tRemove Pack')
    #     print('\t\t' + pack_path)
    #     if os.path.exists(pack_path) and os.path.isdir(pack_path) == True:
    #         shutil.rmtree(pack_path)
    #         return True
    #     return False


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
    print(' * ', sys._getframe().f_code.co_name)
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

    return p_id

def delete_pack(p_id):
    print(' * ',sys._getframe().f_code.co_name)
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
    return pack_name

def get_all_replies(p_id):
    print(' * ',sys._getframe().f_code.co_name)
    sql = 'SELECT * FROM reply WHERE p_id=%s'

    result = []
    db = _login_as_visitor()
    with db.cursor() as cursor:
        cursor.execute(sql, (p_id))
        result = cursor.fetchall()
    db.close()

    return result

def get_pack_path(sex, age):
    print(' * ',sys._getframe().f_code.co_name)
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
    print(' * ',sys._getframe().f_code.co_name)
    result = False

    print(' * Testing args..')
    print('\t', name)
    print('\t', email)
    print('\t', sex)
    print('\t', age)
    print('\t', no)
    print('\t', phone)
    if (Tool.check_name(name) and Tool.check_email(email) and Tool.check_sex(sex) and Tool.check_age(age)
        and Tool.check_no(no) and Tool.check_phone(phone)) == True:
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