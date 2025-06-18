"""
Flexible authentication allowing either API key or JWT token
"""
from typing import Optional, Union
from fastapi import HTTPException, Security, Depends, status
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials

from auth.jwt_auth import get_current_user, CurrentUser
from config import settings

# Security schemes
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)


async def get_api_key_user(api_key: Optional[str] = Security(api_key_header)) -> Optional[CurrentUser]:
    """Validate API key and return a user object"""
    if not api_key:
        return None
    
    # Check against configured API keys
    valid_keys = settings.API_KEYS
    if not valid_keys:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API key validation not configured"
        )
    
    if api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    # Return a system user for API key auth
    return CurrentUser(
        id="api_key_user_001",
        user_id="api_key_user",
        username="api_key_user",
        email="api@flash.ai",
        is_active=True,
        is_admin=False,
        is_superuser=False,
        roles=["api_user"]
    )


async def get_current_user_flexible(
    api_key_user: Optional[CurrentUser] = Depends(get_api_key_user),
    bearer_auth: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme)
) -> CurrentUser:
    """
    Allow authentication via either API key or JWT token.
    API key takes precedence if both are provided.
    """
    # Bypass authentication in development if DISABLE_AUTH is set
    if settings.DISABLE_AUTH and settings.is_development():
        return CurrentUser(
            id="dev_user_001",
            user_id="dev_user",
            username="development_user",
            email="dev@flash.ai",
            is_active=True,
            is_admin=True,  # Grant admin access in dev mode
            is_superuser=True,
            roles=["admin", "api_user", "developer"]
        )
    
    # Try API key first
    if api_key_user:
        return api_key_user
    
    # Try JWT token
    if bearer_auth and bearer_auth.credentials:
        try:
            return await get_current_user(bearer_auth.credentials)
        except HTTPException:
            pass
    
    # No valid authentication provided
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required. Provide either API key or JWT token.",
        headers={"WWW-Authenticate": "Bearer"},
    )


# Convenience dependency for endpoints that should allow both auth methods
FlexibleAuth = Depends(get_current_user_flexible)