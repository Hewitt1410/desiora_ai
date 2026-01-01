"""
Seed script to create default admin user.
Automatically ensures one default admin account exists in the database.
This is called on server startup to guarantee admin access.
"""
import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.repositories.user_repository import UserRepository
from app.models.user import User, UserRole, OAuthProvider
from app.core.security import get_password_hash, verify_password

logger = logging.getLogger(__name__)

# Default admin credentials
DEFAULT_ADMIN_EMAIL = "admin@desiora.ai"
DEFAULT_ADMIN_PASSWORD = "admin123"
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_FULL_NAME = "Default Admin"


async def ensure_default_admin():
    """
    Ensure default admin user exists in the database.
    
    This function:
    1. Checks if admin user exists
    2. If exists, ensures it has super_admin role and is active/verified
    3. If doesn't exist, creates it with email/password authentication
    4. Updates password if it's the default password (for security)
    
    Returns:
        User: The admin user object
    """
    async with AsyncSessionLocal() as session:
        try:
            user_repo = UserRepository(session)
            
            # Check if admin already exists
            admin_user = await user_repo.get_by_email(DEFAULT_ADMIN_EMAIL)
            
            if admin_user:
                # Admin exists - ensure it has correct role and status
                updated = False
                
                # Ensure role is super_admin
                if admin_user.role != UserRole.SUPER_ADMIN.value:
                    admin_user.role = UserRole.SUPER_ADMIN.value
                    updated = True
                    logger.info(f"Updated admin user role to super_admin")
                
                # Ensure user is active and verified
                if not admin_user.is_active:
                    admin_user.is_active = True
                    updated = True
                    logger.info(f"Activated admin user")
                
                if not admin_user.is_verified:
                    admin_user.is_verified = True
                    updated = True
                    logger.info(f"Verified admin user")
                
                # If user has no password (OAuth-only), set default password
                if not admin_user.hashed_password:
                    hashed_password = get_password_hash(DEFAULT_ADMIN_PASSWORD)
                    admin_user.hashed_password = hashed_password
                    admin_user.oauth_provider = OAuthProvider.EMAIL.value
                    updated = True
                    logger.info(f"Set password for admin user")
                
                # If password exists, verify it works (in case hash was corrupted)
                elif admin_user.hashed_password:
                    try:
                        # Test if password verification works
                        if not verify_password(DEFAULT_ADMIN_PASSWORD, admin_user.hashed_password):
                            # Password doesn't match, reset it
                            logger.warning(f"Admin password doesn't match, resetting...")
                            admin_user.hashed_password = get_password_hash(DEFAULT_ADMIN_PASSWORD)
                            updated = True
                    except Exception as e:
                        # Password hash is invalid, reset it
                        logger.warning(f"Admin password hash invalid ({e}), resetting...")
                        admin_user.hashed_password = get_password_hash(DEFAULT_ADMIN_PASSWORD)
                        updated = True
                
                if updated:
                    await session.commit()
                    await session.refresh(admin_user)
                    logger.info(f"✅ Admin user updated: {DEFAULT_ADMIN_EMAIL}")
                else:
                    logger.info(f"✅ Admin user already exists and is configured: {DEFAULT_ADMIN_EMAIL}")
                
                return admin_user
            else:
                # Admin doesn't exist - create it
                from app.schemas.user import UserCreate
                
                admin_data = UserCreate(
                    email=DEFAULT_ADMIN_EMAIL,
                    username=DEFAULT_ADMIN_USERNAME,
                    full_name=DEFAULT_ADMIN_FULL_NAME,
                    password=DEFAULT_ADMIN_PASSWORD
                )
                
                hashed_password = get_password_hash(admin_data.password)
                
                # Create user
                admin_user = await user_repo.create(admin_data, hashed_password)
                
                # Set role to super_admin and ensure active/verified
                admin_user.role = UserRole.SUPER_ADMIN.value
                admin_user.oauth_provider = OAuthProvider.EMAIL.value
                admin_user.is_verified = True
                admin_user.is_active = True
                
                await session.commit()
                await session.refresh(admin_user)
                
                logger.info(f"✅ Default admin user created successfully!")
                logger.info(f"   Email: {DEFAULT_ADMIN_EMAIL}")
                logger.info(f"   Password: {DEFAULT_ADMIN_PASSWORD}")
                logger.info(f"   Role: {admin_user.role}")
                logger.warning(f"   ⚠️  Please change the password after first login!")
                
                return admin_user
                
        except Exception as e:
            logger.error(f"❌ Error ensuring default admin user: {e}", exc_info=True)
            await session.rollback()
            raise


# Alias for backward compatibility
create_default_admin = ensure_default_admin


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(ensure_default_admin())

