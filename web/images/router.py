from fastapi import APIRouter, Depends, UploadFile
from shutil import copyfileobj
from os import path
from web.images.publish import publish_img_to_queue
from web.users.dependencies import get_current_user
from web.users.schemas import UserSchema


router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"]
    )

@router.post("/avatars")
async def add_user_avatar(file: UploadFile, current_user: UserSchema = Depends(get_current_user)):
    image_path = f"web/static/images/{current_user.id}.jpg"
    image_abs_path = path.abspath(image_path)
    
    with open(image_path, '+bw') as f:
        copyfileobj(file.file, f)
        
    data = {
        "user_id": current_user.id,
        "img_path": image_abs_path
    }
    
    await publish_img_to_queue(data)