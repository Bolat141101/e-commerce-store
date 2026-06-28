ARG BASE_IMAGE=python:3.12-slim
FROM ${BASE_IMAGE}

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/models.py .
COPY app/schemas.py .
COPY app/routes.py .
COPY app/logger_config.py .

EXPOSE 5000

CMD ["python", "routes.py"]
