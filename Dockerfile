# Build stage
FROM python:3.10-slim as build-stage
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --jobs=4 --max-workers=4 -r requirements.txt
COPY . .

# Runtime stage
FROM python:3.10-slim
RUN adduser --disabled-password --no-create-home app
WORKDIR /app
COPY --from=build-stage /app /app
RUN pip install --no-cache-dir --jobs=4 --max-workers=4 -r requirements.txt

ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE $PORT
USER app

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
    CMD curl -f http://localhost:$PORT/health || exit 1

CMD ["uvicorn", "main:app", "--host", "${HOST}", "--port", "${PORT}"]