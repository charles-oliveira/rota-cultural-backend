import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db

load_dotenv()

def init_firebase():
    if not firebase_admin._apps:
        cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
        db_url = os.getenv("FIREBASE_DATABASE_URL")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': db_url
        })