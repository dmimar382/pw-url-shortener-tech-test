FROM python:3.11-slim-bullseye

WORKDIR /app

COPY ../../requirements.txt /app
RUN pip install --no-cache -r /app/requirements.txt

COPY ./services/http-api/ /app
COPY ./libs /app/libs


ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "server:app"]
