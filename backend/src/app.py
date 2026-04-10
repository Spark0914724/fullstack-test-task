from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.files import router as files_router
from src.routers.alert import router as alerts_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files_router)
app.include_router(alerts_router)
