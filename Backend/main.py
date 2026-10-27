from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from routers.user import router as user_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://192.168.1.7:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)