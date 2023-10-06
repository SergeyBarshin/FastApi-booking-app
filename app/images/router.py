from fastapi import APIRouter, UploadFile
import shutil

from app.tasks.tasks import procces_pic

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"],
)

@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    im_path = f"app/static/images/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    procces_pic.delay(im_path)