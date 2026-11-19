FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY configs ./configs
COPY feature_repo ./feature_repo
RUN pip install --upgrade pip && pip install .
RUN mkdir -p data/raw data/processed models reports
EXPOSE 8000
CMD ["uvicorn", "fraud_platform.api:app", "--host", "0.0.0.0", "--port", "8000"]
