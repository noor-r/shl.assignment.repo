FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Install CPU-only torch first to avoid pulling the massive CUDA build (~1.5GB saved)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the sentence-transformers model at build time so cold starts are instant
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

COPY . .

# Use $PORT if Render injects it, otherwise fall back to 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
