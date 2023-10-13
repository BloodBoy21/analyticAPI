import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os
from datetime import timedelta

credentials_certificate = {
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv(
        "FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"
    ),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
    "auth_provider_x509_cert_url": os.getenv(
        "FIREBASE_AUTH_PROVIDER_X509_CERT_URL",
        "https://www.googleapis.com/oauth2/v1/certs",
    ),
    "client_x509_cert_url": os.getenv(
        "FIREBASE_CLIENT_X509_CERT_URL",
        "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-gkjdj%40analytic-services-b362e.iam.gserviceaccount.com",
    ),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN", "googleapis.com"),
}
print(credentials_certificate)
cred = credentials.Certificate(credentials_certificate)
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
