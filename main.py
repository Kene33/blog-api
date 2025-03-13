import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import api_router


app = FastAPI(title="BLOG AP123I", description="CRUD API for blog.")
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host = "127.0.0.1", port = 1234)
