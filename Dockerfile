FROM python:3.10

RUN mkdir /booking

WORKDIR /booking

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN ["chmod", "a+x", "./docker/app.sh"] 
RUN ["chmod", "a+x", "./docker/celery.sh"] 


CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000" ]