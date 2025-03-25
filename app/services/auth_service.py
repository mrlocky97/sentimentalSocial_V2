from passlib.context import CryptContext
from pymongo.database import Database
from fastapi import HTTPException
from app.models.user import UserDB, UserCreate, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    async def authenticate_user(self, email: str, password: str) -> UserDB:
        user = await self.db.users.find_one(UserDB.email == email)
        if not user:# si el usuario no existe
            raise HTTPException(status_code=401, detail="Invalid user does not exist")
        if not self.verify_password(password, user.password_hash): # si la contraseña no coincide
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return UserDB(**user)
    
    def dtoUserResponse(user: UserDB) -> UserResponse:
        test = UserResponse(
            email = user.email,
            is_active = user.is_active
        )
        print("IMPORTANT -> ", test)
        print("IMPORTANT user -> ", user)
        breakpoint()
        return UserResponse(
            email = user.email,
            is_active = user.is_active
        )