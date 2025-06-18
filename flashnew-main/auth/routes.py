"""
Authentication routes for FLASH Platform
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth.jwt_auth import (
    AuthService, Token, UserCreate, UserLogin,
    CurrentUser, get_current_user, get_current_active_user
)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=Token)
async def register(user_create: UserCreate):
    """Register new user"""
    # For demo, using mock service
    auth_service = AuthService(None)
    
    # Check if user exists (in real app, check database)
    # For demo, just create user
    try:
        user = await auth_service.create_user(user_create)
        # Auto-login after registration
        return await auth_service.login(user.username, user_create.password)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with username and password"""
    auth_service = AuthService(None)
    
    try:
        return await auth_service.login(form_data.username, form_data.password)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    """Refresh access token"""
    auth_service = AuthService(None)
    return await auth_service.refresh_token(refresh_token)


@router.get("/me", response_model=CurrentUser)
async def get_me(current_user: CurrentUser = Depends(get_current_active_user)):
    """Get current user info"""
    return current_user


@router.post("/logout")
async def logout(current_user: CurrentUser = Depends(get_current_active_user)):
    """Logout user (client should delete tokens)"""
    # In a real app, you might blacklist the token
    return {"message": "Successfully logged out"}