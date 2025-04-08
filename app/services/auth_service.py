from passlib.context import CryptContext
from pymongo.database import Database
from fastapi import HTTPException
from app.core.jwt_utils import create_access_token
from app.models.user import UserDB, UserCreate, UserResponse, UserBase

pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=12, deprecated="auto")

class AuthService:
    # Constructor
    def __init__(self, db: Database): # Database object
        self.db = db
    
    # Método para hashear la contraseña
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    # Método para verificar la contraseña
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # Método para crear un usuario
    async def create_user(self, user_data: UserCreate) -> UserDB:
        # verufuca si el usuario ya existe
        if await self.db.users.find_one(UserDB.email == user_data.email):
            raise HTTPException(status_code=400, detail="User already registered")
        
        # crea un diccionario con los datos del usuario
        user_dict = user_data.model_dump(exclude={"password"})
        # hashea la contraseña
        user_dict["password_hash"] = self.hash_password(user_data.password)
        
        user = UserDB(**user_dict)
        await user.insert()
        return user
    
    # Método para autenticar un usuario
    async def authenticate_user(self, email: str, password: str) -> dict:
        user = await self.db.users.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not self.verify_password(password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"sub": user["email"]})
        return {"access_token": token, "token_type": "bearer"}

    @staticmethod
    def dtoUserResponse(user: UserDB) -> UserResponse:
        return UserResponse(
            message="User created successfully", 
            user=UserBase(
                username=user.username,
                email=user.email
            )
        )