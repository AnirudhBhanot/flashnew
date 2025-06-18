"""
JWT Authentication System for FLASH Platform
Provides user authentication and session management
"""
import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field

logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)


class Token(BaseModel):
    """Token response model"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int = Field(default=ACCESS_TOKEN_EXPIRE_MINUTES * 60)


class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None
    user_id: Optional[str] = None
    email: Optional[str] = None
    roles: list[str] = []


class UserCreate(BaseModel):
    """User creation request"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login request"""
    username: str
    password: str


class UserInDB(BaseModel):
    """User stored in database"""
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    roles: list[str] = []
    created_at: datetime
    last_login: Optional[datetime] = None


class CurrentUser(BaseModel):
    """Current authenticated user"""
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    roles: list[str] = []
    is_superuser: bool = False
    is_active: bool = True
    is_admin: bool = False
    user_id: Optional[str] = None  # Alternative ID field


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise JWTError("Invalid token payload")
        
        return TokenData(
            username=username,
            user_id=payload.get("user_id"),
            email=payload.get("email"),
            roles=payload.get("roles", [])
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> CurrentUser:
    """Get current user from JWT token"""
    from config import settings
    
    # Bypass authentication in development if DISABLE_AUTH is set
    if settings.DISABLE_AUTH and settings.is_development():
        return CurrentUser(
            id="dev_user",
            username="development_user",
            email="dev@flash.ai",
            full_name="Development User",
            roles=["admin", "api_user", "developer"],
            is_superuser=True
        )
    
    # If no token provided, raise unauthorized
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = decode_token(token)
    
    # In a real app, you would fetch user from database here
    # For now, return user from token data
    return CurrentUser(
        id=token_data.user_id or "unknown",
        username=token_data.username,
        email=token_data.email or "",
        roles=token_data.roles
    )


async def get_current_active_user(
    current_user: CurrentUser = Depends(get_current_user)
) -> CurrentUser:
    """Ensure user is active"""
    from config import settings
    
    # Bypass authentication in development if DISABLE_AUTH is set
    if settings.DISABLE_AUTH and settings.is_development():
        return CurrentUser(
            id="dev_user",
            username="development_user",
            email="dev@flash.ai",
            full_name="Development User",
            roles=["admin", "api_user", "developer"],
            is_superuser=True
        )
    
    # In a real app, check if user is active in database
    return current_user


def require_role(required_role: str):
    """Dependency to require specific role"""
    async def role_checker(current_user: CurrentUser = Depends(get_current_active_user)):
        if required_role not in current_user.roles and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker


def require_superuser(current_user: CurrentUser = Depends(get_current_active_user)):
    """Dependency to require superuser"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superuser access required"
        )
    return current_user


# Authentication service
class AuthService:
    """Authentication service handling user operations"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    async def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        """Authenticate user with username and password"""
        # This is a placeholder - in real app, fetch from database
        # For demo, we'll use a hardcoded user
        if username == "demo" and password == "demo123456":
            return UserInDB(
                id="demo-user-id",
                username="demo",
                email="demo@flash-platform.com",
                full_name="Demo User",
                hashed_password=get_password_hash("demo123456"),
                roles=["user"],
                created_at=datetime.now(timezone.utc)
            )
        return None
    
    async def create_user(self, user_create: UserCreate) -> UserInDB:
        """Create new user"""
        # In real app, save to database
        hashed_password = get_password_hash(user_create.password)
        
        user = UserInDB(
            id=secrets.token_urlsafe(16),
            username=user_create.username,
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
            roles=["user"],
            created_at=datetime.now(timezone.utc)
        )
        
        # Save to database here
        logger.info(f"Created user: {user.username}")
        return user
    
    async def login(self, username: str, password: str) -> Token:
        """Login user and return tokens"""
        user = await self.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Update last login
        user.last_login = datetime.now(timezone.utc)
        
        # Create tokens
        token_data = {
            "sub": user.username,
            "user_id": user.id,
            "email": user.email,
            "roles": user.roles
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )
    
    async def refresh_token(self, refresh_token: str) -> Token:
        """Refresh access token using refresh token"""
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != "refresh":
                raise JWTError("Invalid token type")
            
            # Create new access token
            token_data = {
                "sub": payload.get("sub"),
                "user_id": payload.get("user_id"),
                "email": payload.get("email"),
                "roles": payload.get("roles", [])
            }
            
            access_token = create_access_token(token_data)
            
            return Token(access_token=access_token)
            
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )