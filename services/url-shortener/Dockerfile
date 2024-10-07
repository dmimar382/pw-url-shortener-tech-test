# Dockerfile-url-shortener
FROM python:3.11-slim-bullseye

WORKDIR /app

# Install dependencies
COPY ../../requirements.txt /app
RUN pip install --no-cache -r /app/requirements.txt

# Copy the app source code
COPY ./services/url-shortener/ /app

# Expose the port that FastAPI runs on
EXPOSE 8001

# Command to run FastAPI
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8001", "url_shortener_service:app"]
