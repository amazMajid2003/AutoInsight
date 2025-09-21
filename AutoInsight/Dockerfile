# 1. Use lightweight Python base image
FROM python:3.11-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Install system dependencies (needed for pandas, GUI, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-tk \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements file first (for better caching)
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# 6. Copy project files (app/, data/, GUI/, etc.)
COPY app/ app/
COPY data/ data/
COPY GUI/ GUI/

# 7. Expose FastAPI default port
EXPOSE 8000

# 8. Start FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
