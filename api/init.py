from fastapi import APIRouter

from api.routes import analytics, documents

api_router = APIRouter()
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
