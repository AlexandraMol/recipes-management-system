import firebase_admin
from firebase_admin import credentials, firestore, auth, storage

cred = credentials.Certificate(
    "firebase/serviceAccountKey.json"
)

firebase_admin.initialize_app(cred, {
    "storageBucket": "be-your-own-chef-b906f.firebasestorage.app"
})
db = firestore.client()
firebase_auth = auth
firebase_storage = storage