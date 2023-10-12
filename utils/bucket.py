import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os
from datetime import timedelta

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred, {"storageBucket": os.getenv("FIREBASE_BUCKET")})

bucket = storage.bucket()


def upload_file(data: bytes, filename: str, content_type: str) -> str:
    blob = bucket.blob(filename)
    blob.upload_from_string(data, content_type=content_type)
    public_url = blob.generate_signed_url(version="v4", expiration=timedelta(weeks=1))
    url = blob.public_url
    return {
        "public_url": public_url,
        "url": url,
        "filename": filename,
        "content_type": content_type,
    }


def download_file(filename: str) -> bytes:
    blob = bucket.blob(filename)
    return blob.download_as_string()
