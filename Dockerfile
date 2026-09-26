FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .
ENV FOXSHIELD_DB_PATH=/app/data/foxshield.db
RUN mkdir -p /app/data
EXPOSE 8000 8501
CMD ["uvicorn","foxshield.api.main:app","--host","0.0.0.0","--port","8000"]
