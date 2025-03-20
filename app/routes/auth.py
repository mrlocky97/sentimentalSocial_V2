from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

# Register endpoint
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_db) # AuthService object
):
    try:
        user = await auth_service.create_user(user_data)
        return {"message": "User created successfully", "user": user}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# Login endpoint
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(lambda: AuthService(get_db())) # AuthService object
):
    try:
        user = await auth_service.authenticate_user(form_data.username, form_data.password)
        return {
            "message": "Login successful", 
            "user": user,
            "is_active": user.is_active
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )