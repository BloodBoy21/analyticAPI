from fastapi import FastAPI 
from database.db import engine, db
from api.init import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="miLocal")
app.include_router(api_router, prefix="/api", tags=["api","v1"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    print("Starting up")
    db.metadata.create_all(bind=engine, checkfirst=True)


@app.get("/")
def root():
    return {"status": "ok"}