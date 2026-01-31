FROM python:3.10-slim-buster

WORKDIR /app

copy . /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3","app.py"]

