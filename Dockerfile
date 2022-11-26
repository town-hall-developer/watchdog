FROM --platform=linux/amd64 python:3.8-slim-buster
FROM python:3.8

WORKDIR .
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "-m", "gunicorn", "-k", \
"uvicorn.workers.UvicornWorker", "--access-logfile", "./gunicorn-access.log", \
"main:app", "--preload", "--bind", "0.0.0.0:8000", "--workers", "2"]