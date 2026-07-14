FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# exec + sh -c so ${PORT} expands at runtime (hosts like Render assign the port)
# while uvicorn still runs as PID 1 and receives SIGTERM for graceful shutdown.
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]


