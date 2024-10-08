# Dockerfile-url-shortener
FROM python:3.11-slim-bullseye

WORKDIR /app

# Install dependencies
COPY ../../requirements.txt /app
RUN pip install --no-cache -r /app/requirements.txt

# Copy the app source code
COPY ./services/url-grpc-server/ /app
COPY ./libs/protocols /app/libs/protocols
COPY ./libs /app/libs

ENV PYTHONPATH=/app/libs/protocols

EXPOSE 50051

CMD ["python", "server.py"]
