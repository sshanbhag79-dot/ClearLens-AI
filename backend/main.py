from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import scan, community, log, user, chat
import os

app = FastAPI(title="BioFilter API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(scan.router)
app.include_router(community.router)
app.include_router(log.router)
app.include_router(user.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "BioFilter API is running"}
