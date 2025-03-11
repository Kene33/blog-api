import uvicorn

from fastapi import FastAPI
from src.api import main_router

app = FastAPI(title="BLOG API", description="CRUD API for blog.")
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=1234)
