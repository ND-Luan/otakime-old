from pyrebaseLib.pyrebase import pyrebase

config = {
  "apiKey": "AIzaSyBsWfL_ws_g-lu_PJin0cG48yH_M38PhX4",
  "authDomain": "otakime-dc208.firebaseapp.com",
  "databaseURL": "https://otakime-dc208-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "otakime-dc208",
  "storageBucket": "otakime-dc208.appspot.com",
  "messagingSenderId": "1022690635838",
  "appId": "1:1022690635838:web:f0f624a2f6d0f64cea616f",
  "measurementId": "G-8RP2DN4733",
  "serviceAccount":"servicesAccountKey.json"

}
firebase = pyrebase.initialize_app(config)
email = "mail.otakime@gmail.com"
password = "otakime30"
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(email,password)
storage = firebase.storage()

db = firebase.database()












