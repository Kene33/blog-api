import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles

from src.api.users import security

router = APIRouter()

UPLOAD_DIR = "src/database/images/posts"
os.makedirs(UPLOAD_DIR, exist_ok=True)


router.mount("/media", StaticFiles(directory=UPLOAD_DIR), name="media")

@router.post("/upload_media", dependencies=[Depends(security.access_token_required)])
async def upload_media(file: UploadFile = File(...)):
    try:
        ext = os.path.splitext(file.filename)[1]
        if ext.lower() not in [".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mov", ".avi"]:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    
        new_filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, new_filename)

        # Сохраняем файл
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        avatar_url = f"{UPLOAD_DIR}/{new_filename}"
        return {"ok": True, "avatar_url": avatar_url}
    except:
        return {"ok": False, "avatar_url": None}
