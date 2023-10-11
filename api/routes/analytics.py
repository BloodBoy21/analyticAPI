from fastapi import APIRouter, Depends
from middleware.user_auth import auth_user
from models.process import AnalyticProcess

router = APIRouter()


@router.post("/")
def create_analytics():
    pass


@router.post("/process/{id}")
def process_analytics(process: AnalyticProcess = Depends(auth_user)):
    pass


@router.patch("/process/{id}")
def add_data_to_analytics(process: AnalyticProcess = Depends(auth_user)):
    pass


@router.get("/process/{id}")
def get_analytics(process: AnalyticProcess = Depends(auth_user)):
    pass
