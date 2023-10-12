from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from middleware.user_auth import auth_user
from models.process import AnalyticProcess
from utils import bucket
from services.analytic_services import set_file

router = APIRouter()


@router.post("/")
def upload_document(
    file: UploadFile = File(...), process: AnalyticProcess = Depends(auth_user)
) -> dict:
    file_name = f"process_{process.process_id}.{file.filename.split('.')[-1]}"
    bytes = file.file.read()
    file_data = bucket.upload_file(bytes, file_name, file.content_type)
    set_file(process.process_id, file_data["filename"])
    return {"url": file_data["public_url"]}
