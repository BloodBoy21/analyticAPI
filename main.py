from fastapi import FastAPI
from database.db import engine, db
from api.init import api_router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="miLocal")
app.include_router(api_router, prefix="/api", tags=["api", "v1"])
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


if __name__ == "__main__":
    import uvicorn

    port = os.getenv("PORT", 3000)
    uvicorn.run(app="main:app", host="0.0.0.0", port=port, reload=True)
