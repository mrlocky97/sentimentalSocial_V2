from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.jwt_utils import decode_access_token
from app.database import get_db
from app.models.user import UserDB
from app.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Dependency to get the database object
def get_auth_service(db = Depends(get_db)):
    return AuthService(db)

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    # Decodificar el token para obtener la información del usuario
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas"
        )

    # Obtener el identificador (en este caso, el email) del payload
    email = payload["sub"]    
    
    # Realizar la búsqueda en la base de datos (utilizando Beanie, es asíncrono)
    user = await UserDB.find_one(UserDB.email == email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario no existe o ya no es válido"
        )
    return user