"""
Fix for the /predict endpoint validation issue
"""

from fastapi import Body
from typing import Annotated

# Option 1: Explicitly mark data as coming from request body
async def predict_fixed_v1(
    request: Request, 
    data: Annotated[StartupData, Body()],  # Explicitly mark as body parameter
    current_user: CurrentUser = Depends(get_current_user_flexible)
):
    """Fixed version with explicit Body annotation"""
    # ... rest of the function remains the same
    pass


# Option 2: Change parameter order (body params before dependencies)
async def predict_fixed_v2(
    data: StartupData,  # Body parameter first
    request: Request,
    current_user: CurrentUser = Depends(get_current_user_flexible)
):
    """Fixed version with reordered parameters"""
    # ... rest of the function remains the same
    pass


# Option 3: Use a different model without extra='allow'
class StartupDataStrict(StartupData):
    """Strict version of StartupData that doesn't allow extra fields"""
    class Config:
        extra = 'forbid'  # Don't allow extra fields
        validate_assignment = True


# Option 4: Add validation to ensure we're getting the right data
async def predict_fixed_v4(
    request: Request, 
    data: StartupData,
    current_user: CurrentUser = Depends(get_current_user_flexible)
):
    """Fixed version with additional validation"""
    # Check if we received user data by mistake
    data_dict = data.dict()
    if 'user_id' in data_dict or 'username' in data_dict:
        raise HTTPException(
            status_code=400,
            detail="Invalid request: received user data instead of startup data"
        )
    
    # ... rest of the function remains the same
    pass