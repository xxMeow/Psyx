import PsyxDB

def GetPackID(pack_name):
    sql = 'SELECT p_id FROM pack WHERE folder_name="{}"'\
        .format(pack_name)
    # SELECT p_id FROM pack WHERE folder_name="catdog";


def InfoPacks(pack_name):
    sql = 'SELECT * FROM reply WHERE folder_name="{}"'\
        .format(pack_name)
    replys = {}

    db = PsyxDB.loginAsAdmin()
    with db.cursor() as cursor:
        cursor.execute(sql)
        replys = cursor.fetchall()
    db.close()

    return replys

def GetReply(packname):
    sql = 'SELECT pack.p_id, pack.folder_name, reply.* FROM pack, reply WHERE pack.folder_name="{}"'\
        format(packname)
    replys =

def AddPack():
    return False

def RemovePack():
    return None
