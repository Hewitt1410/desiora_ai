# AI Worker for Room Design

GPU-enabled Celery worker for processing room design jobs.

## Pipeline

1. **Load original image** - Fetch room image from URL
2. **Segmentation using SAM** - Segment room elements using Segment Anything Model
3. **Depth estimation** - Estimate depth map for 3D understanding
4. **Prompt generation** - Generate design prompt from style preferences
5. **Stable Diffusion XL img2img** - Generate redesigned room
6. **Upscale using Real-ESRGAN** - Enhance image quality
7. **Save output to storage** - Upload results to S3 or local storage

## Setup

### Prerequisites

- NVIDIA GPU with CUDA support
- Docker and Docker Compose
- Redis (for Celery broker)

### Environment Variables

Add to `.env`:

```env
# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# AI Worker
AI_WORKER_DEVICE=cuda
AI_WORKER_MODEL_CACHE_DIR=/app/models
AI_WORKER_OUTPUT_DIR=/app/outputs

# Storage
STORAGE_BACKEND=s3
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket
```

### Build and Run

```bash
# Build worker image
docker-compose -f docker-compose.worker.yml build

# Start worker
docker-compose -f docker-compose.worker.yml up -d

# View logs
docker-compose -f docker-compose.worker.yml logs -f celery-worker
```

### Local Development

```bash
# Install dependencies
pip install -r requirements-worker.txt

# Start Redis
docker run -d -p 6379:6379 redis:7-alpine

# Run Celery worker
celery -A app.core.celery_app worker --loglevel=info
```

## Model Integration

The worker includes placeholder implementations for all models. To use actual models:

1. **SAM (Segment Anything Model)**
   - Download model weights from [Meta AI](https://github.com/facebookresearch/segment-anything)
   - Place in `/app/models/`
   - Uncomment SAM loading code in `app/workers/models.py`

2. **Depth Estimation**
   - Use DPT or MiDaS models
   - Install: `pip install transformers timm`
   - Uncomment depth model loading code

3. **Stable Diffusion XL**
   - Install: `pip install diffusers accelerate xformers`
   - Models will be downloaded automatically on first use
   - Uncomment SDXL loading code

4. **Real-ESRGAN**
   - Install: `pip install basicsr realesrgan`
   - Download model weights
   - Uncomment upscaler loading code

## Style Prompts

Supported styles:
- `modern` - Clean lines, contemporary design
- `minimalist` - Sparse, uncluttered space
- `rustic` - Wooden, vintage, cozy
- `scandinavian` - Light colors, hygge atmosphere
- `industrial` - Exposed brick, metal fixtures
- `bohemian` - Eclectic, vibrant, artistic
- `traditional` - Classic, elegant, formal
- `contemporary` - Current trends, mixed styles

## Usage

The worker automatically processes jobs from the queue. Jobs are created via the API:

```python
POST /api/designs
{
  "job_type": "room_design",
  "prompt": "Modern living room",
  "parameters": {
    "image_url": "https://example.com/room.jpg",
    "style": "modern",
    "room_type": "living_room"
  }
}
```

## Monitoring

- Check Celery status: `celery -A app.core.celery_app inspect active`
- View task results: `celery -A app.core.celery_app result <task_id>`
- Monitor with Flower: `celery -A app.core.celery_app flower`

