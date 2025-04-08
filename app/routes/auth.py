import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.dependencies import get_auth_service
from app.models.user import UserCreate, UserDB, UserResponse
from app.services.auth_service import AuthService

logger = logging.getLogger("auth")
logger.setLevel(logging.INFO)
# Se puede agregar un handler si no se ha configurado de forma global
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

router = APIRouter(prefix="/auth", tags=["auth"])

# Register endpoint
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service) # AuthService object
):
    try:
        user: UserDB = await auth_service.create_user(user_data)
        logger.info(f"Usuario registrado: {user.email}")
        return AuthService.dtoUserResponse(user)
    except Exception as e:
        logger.error(f"Error al registrar usuario: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# Login endpoint
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service) # AuthService object
):
    try:
        token_data = await auth_service.authenticate_user(form_data.username, form_data.password)
        logger.info(f"Usuario autenticado: {form_data.username}")
        return token_data
    except HTTPException as e:
        logger.error(f"Login fallido para usuario: {form_data.username} - {e.detail}")
        raise e
    except Exception as e:
        logger.exception(f"Error interno durante el login para usuario: {form_data.username}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
