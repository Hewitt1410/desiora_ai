"""
Seed script to create default admin user.
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.repositories.user_repository import UserRepository
from app.models.user import User, UserRole
from app.core.security import get_password_hash


async def create_default_admin():
    """
    Create default admin user if it doesn't exist.
    
    Default credentials:
    - Email: admin@desiora.ai
    - Password: admin123
    - Role: super_admin
    """
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        
        # Check if admin already exists
        admin_email = "admin@desiora.ai"
        existing_admin = await user_repo.get_by_email(admin_email)
        
        if existing_admin:
            print(f"Admin user already exists: {admin_email}")
            return existing_admin
        
        # Create admin user directly with super_admin role
        from app.schemas.user import UserCreate
        
        admin_data = UserCreate(
            email=admin_email,
            username="admin",
            full_name="Default Admin",
            password="admin123"  # Will be hashed
        )
        
        hashed_password = get_password_hash(admin_data.password)
        
        # Create user
        admin_user = await user_repo.create(admin_data, hashed_password)
        
        # Update role to super_admin and set verified/active
        admin_user.role = UserRole.SUPER_ADMIN
        admin_user.is_verified = True
        admin_user.is_active = True
        
        await session.commit()
        await session.refresh(admin_user)
        
        print(f"✅ Default admin user created successfully!")
        print(f"   Email: {admin_email}")
        print(f"   Password: admin123")
        print(f"   Role: {admin_user.role}")
        print(f"   ⚠️  Please change the password after first login!")
        
        return admin_user


if __name__ == "__main__":
    asyncio.run(create_default_admin())

