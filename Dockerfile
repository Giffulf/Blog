FROM python:3.11

COPY requirements/base.txt /src/requirements/base.txt
COPY requirements/production.txt /src/requirements/production.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements/production.txt

COPY ./src /src

CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
