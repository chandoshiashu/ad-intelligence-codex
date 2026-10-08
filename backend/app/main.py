from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.routes.analyze import router as analyze_router

app = FastAPI(title="Ad Intelligence API")


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

app.include_router(analyze_router)


@app.get("/")
def root():
    return {"message": "Ad Intelligence API is running"}
