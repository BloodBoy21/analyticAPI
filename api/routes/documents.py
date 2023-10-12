from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from middleware.user_auth import auth_user
from models.process import AnalyticProcess
from utils import bucket
from services.analytic_services import (
    set_file,
    analyze_data,
    add_data,
    save_anomaly_bytes,
)
from services.anomaly_services import DetectAnomaly

router = APIRouter()


@router.post("/")
def upload_document(
    file: UploadFile = File(...), process: AnalyticProcess = Depends(auth_user)
) -> dict:
    if not file:
        raise HTTPException(status_code=400, detail="File not found")
    allowed_extensions = ["csv", "xlsx"]
    file_type = file.filename.split(".")[-1]
    if file_type not in allowed_extensions:
        raise HTTPException(
            status_code=400, detail=f"File extension not allowed: {file.filename}"
        )
    file_name = f"process_{process.process_id}.{file_type}"
    bytes = file.file.read()
    file_data = bucket.upload_file(bytes, file_name, file.content_type)
    save_anomaly_bytes(bytes, process.process_id)
    set_file(process.process_id, file_data["filename"])
    analyze_data(process, bytes, file_type)
    return {"url": file_data["public_url"]}


@router.post("/add")
def upload_document(
    file: UploadFile = File(...), process: AnalyticProcess = Depends(auth_user)
) -> dict:
    if not file:
        raise HTTPException(status_code=400, detail="File not found")
    allowed_extensions = ["csv", "xlsx"]
    file_type = file.filename.split(".")[-1]
    if file_type not in allowed_extensions:
        raise HTTPException(
            status_code=400, detail=f"File extension not allowed: {file.filename}"
        )
    if file_type != process.file.split(".")[-1]:
        raise HTTPException(
            status_code=400, detail=f"File type not allowed: {file.filename}"
        )
    bytes = file.file.read()
    save_anomaly_bytes(bytes, process.process_id)
    new_data = add_data(process, bytes, file.content_type)
    analyze_data(process, new_data, file_type)
    return {
        "message": "Data added to process",
        "process_id": process.process_id,
        "process_name": process.name,
    }
