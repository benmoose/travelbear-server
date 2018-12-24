FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install gunicorn

COPY requirements*.txt ./
RUN pip install -r requirements.test.txt

COPY . .

EXPOSE 8000
