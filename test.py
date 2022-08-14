from firebase import db,storage,user

db.child("anh hung xa dieu").child("chapter").child("Chap 03").remove(user['idToken'])