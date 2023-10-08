from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_analytics():
    pass

@router.post("process/{id}")
def process_analytics():
    pass
  
@router.patch("process/{id}")
def add_data_to_analytics():
    pass

@router.get("process/{id}")
def get_analytics():
    pass