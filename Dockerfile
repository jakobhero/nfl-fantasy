FROM python:3.9.19-bookworm

COPY . .

RUN pip install -r requirements.txt