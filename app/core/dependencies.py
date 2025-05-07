from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.jwt_utils import decode_access_token
from app.database import get_db
from app.models.user import UserDB
from app.services.auth_service import AuthService
# Import the NLP service dependency provider
from app.core.config import get_nlp_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Auth service injector
def get_auth_service(db = Depends(get_db)):
    return AuthService(db)

# Current user injector
async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas"
        )
    email = payload["sub"]
    user = await UserDB.find_one(UserDB.email == email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario no existe o ya no es válido"
        )
    return user