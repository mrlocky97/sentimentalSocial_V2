from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.jwt_utils import decode_access_token
from app.database import get_db
from app.models.user import UserDB, UserRole
from app.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Auth service injector
def get_auth_service(db = Depends(get_db)):
    return AuthService(db)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDB:
    payload = decode_access_token(token)
    if not payload or "sub" not in payload or "role" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    user = await UserDB.find_one(UserDB.email == payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    return user

async def require_admin(current_user: UserDB = Depends(get_current_user)) -> UserDB:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permisos de administrador requeridos")
    return current_user

async def require_readonly_or_admin(current_user: UserDB = Depends(get_current_user)) -> UserDB:
    if current_user.role not in {UserRole.READONLY, UserRole.ADMIN}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso de solo lectura o admin requerido")
    return current_user