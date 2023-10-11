from pathlib import Path

from PIL import Image

from app.tasks.celery import celery


@celery.task
def procces_pic(path:str):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000,500))
    im_resized_200_100 = im.resize((200,100))
    im_resized_1000_500.save(f"app/static/images/im_resized_1000_500{im_path.name}")
    im_resized_200_100.save(f"app/static/images/im_resized_200_100{im_path.name}")