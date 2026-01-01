FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    wget \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set Python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Copy requirements
COPY requirements-worker.txt /app/requirements-worker.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-worker.txt

# Copy application code
COPY app /app/app
COPY alembic /app/alembic
COPY alembic.ini /app/

# Create directories
RUN mkdir -p /app/models /app/outputs

# Set environment variables
ENV PYTHONPATH=/app
ENV CUDA_VISIBLE_DEVICES=0
ENV AI_WORKER_DEVICE=cuda
ENV AI_WORKER_MODEL_CACHE_DIR=/app/models
ENV AI_WORKER_OUTPUT_DIR=/app/outputs

# Run Celery worker
CMD ["celery", "-A", "app.core.celery_app", "worker", "--loglevel=info", "--concurrency=1"]


