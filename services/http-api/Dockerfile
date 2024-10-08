FROM python:3.11-slim-bullseye

WORKDIR /app

COPY ../../requirements.txt /app
RUN pip install --no-cache -r /app/requirements.txt

COPY ./services/http-api/ /app
COPY ./libs/protocols /app/libs/protocols
COPY ./libs /app/libs

ENV PYTHONPATH=/app/libs/protocols

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "api-server:app"]
