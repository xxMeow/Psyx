import PsyxDB

def SelectPack(age, gender):
    # Select (age, gender) in DB
    sql = "SELECT folder_name FROM pack WHERE gender={} and age_low<={} AND age_high>={}"\
        .format(gender, age, age)
    packs = {}

    # SELECT folder_name FROM pack WHERE gender=1 and age_low <= 27 AND age_high >= 27;

    db = PsyxDB.loginAsVisitor()
    with db.cursor() as cursor:
        cursor.execute(sql)
        packs = cursor.fetchall()
    db.close()

    return packs

print(SelectPack(gender=1, age=23))