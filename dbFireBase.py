from firebase import db,storage,user

DB = db.get().val()

def getManga():
    DICT = {}
    for key,value in DB.items():
        DICT.update({key:value})
    return DICT