FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
COPY src/ src/
RUN pip install .
CMD ["sh", "-c", "uvicorn baseball_stats.api.main:app --host 0.0.0.0 --port $PORT"]