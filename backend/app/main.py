from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.routes.analyze import router as analyze_router

app = FastAPI(title="Ad Intelligence API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ad-intelligence-codex.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)


@app.get("/")
def root():
    return {"message": "Ad Intelligence API is running"}
