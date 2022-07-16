import pyrebase

config = {
    "apiKey": "AIzaSyBsWfL_ws_g-lu_PJin0cG48yH_M38PhX4",
    "authDomain": "otakime-dc208.firebaseapp.com",
    "projectId": "otakime-dc208",
    "storageBucket": "otakime-dc208.appspot.com",
    "messagingSenderId": "1022690635838",
    "appId": "1:1022690635838:web:f0f624a2f6d0f64cea616f",
    "measurementId": "G-8RP2DN4733"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()