FROM python:3.9.19-bookworm

RUN pip install poetry==1.85

COPY . .

RUN poetry install