FROM python:3.12-slim

WORKDIR /app

COPY healthcheck.py .

USER 10001:10001

CMD ["python", "healthcheck.py"]