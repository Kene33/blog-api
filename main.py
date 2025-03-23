import uvicorn
import asyncio
import authx.exceptions

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.api import api_router
from src.database import posts, users


app = FastAPI(title="BLOG AP123I", description="CRUD API for blog.")
app.include_router(api_router)

@app.exception_handler(authx.exceptions.MissingTokenError)
async def missing_token_exception_handler():
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Вы не вошли в аккаунт"}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://127.0.0.1:4000"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

async def on_startup():
    await posts.create_database()
    await users.create_database()

if __name__ == "__main__":
    asyncio.run(on_startup())
    uvicorn.run("main:app", reload=True, host = "127.0.0.1", port = 4000)
