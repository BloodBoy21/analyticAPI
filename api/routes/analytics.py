from fastapi import APIRouter, Depends, HTTPException
from middleware.user_auth import auth_user
from models.process import AnalyticProcess
from models.process import AnalyticProcessIn, AnalyticProcessOut, AnalyticProcess
import services.analytic_services as analytics_service
from utils.security import verify_jwt

router = APIRouter()


@router.post("/")
def create_analytics(process: AnalyticProcessIn) -> AnalyticProcessOut:
    return analytics_service.create_analytics(process)


@router.post("/process/{id}")
def process_analytics(process: AnalyticProcess = Depends(auth_user)):
    if id != process.process_id:
        raise HTTPException(status_code=403, detail="Not authorized")


@router.patch("/process/{id}")
def add_data_to_analytics(process: AnalyticProcess = Depends(auth_user)):
    if id != process.process_id:
        raise HTTPException(status_code=403, detail="Not authorized")


@router.get("/process")
def get_analytics(token: str = None) -> dict:
    process = verify_jwt(token)
    process = analytics_service.get_service_by_id(process)
    if not process:
        raise HTTPException(status_code=400, detail="Analytics not found")
    data = analytics_service.get_anomaly(process.process_id)
    return {
        "process_id": process.process_id,
        "process_name": process.name,
        "data": data,
    }
