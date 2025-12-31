from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.image_service import ImageService
from app.schemas.image import (
    PresignUploadRequest,
    PresignUploadResponse,
    ImageCreateRequest,
    ImageResponse,
    ConfirmUploadRequest,
)
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/presign-upload", response_model=PresignUploadResponse, status_code=status.HTTP_201_CREATED)
async def presign_upload(
    request: PresignUploadRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Generate presigned S3 upload URL.
    
    Returns a presigned URL that can be used to upload the image directly to S3.
    The client should:
    1. Call this endpoint to get the presigned URL
    2. Upload the image to the presigned URL using PUT request
    3. Call POST /images to confirm the upload and store metadata
    """
    image_service = ImageService(db)
    return await image_service.generate_presigned_upload_url(
        user_id=current_user.id,
        request=request,
    )


@router.post("", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def create_image(
    image_data: ImageCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create image record after upload.
    
    This endpoint should be called after the image has been uploaded to S3 using
    the presigned URL from /presign-upload.
    
    It validates the upload and stores metadata in the database.
    """
    image_service = ImageService(db)
    image = await image_service.create_image_record(
        user_id=current_user.id,
        image_data=image_data,
    )
    return image


@router.post("/confirm-upload", status_code=status.HTTP_200_OK)
async def confirm_upload(
    request: ConfirmUploadRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Confirm image upload and update status.
    
    Alternative endpoint to confirm upload if image was created via presign-upload.
    Body: {"s3_key": "images/user_id/uuid.jpg"}
    """
    image_service = ImageService(db)
    await image_service.confirm_upload(current_user.id, request.s3_key)
    return {"message": "Upload confirmed"}

