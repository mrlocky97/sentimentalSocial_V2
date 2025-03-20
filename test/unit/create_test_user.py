import asyncio
from app.database import connect_db
from app.models.user import UserCreate, UserDB
from app.services.auth_service import AuthService

async def create_test_user():
    # Conectar a la base de datos
    db = connect_db()
    
    auth_service = AuthService(db)
    
    test_user = UserCreate(
        username="test_user",
        email="test@example.com",
        password="SecurePass123!",
        is_active=True
    )
    
    try:
        user = await auth_service.create_user(test_user)
        print(f"✅ Usuario de prueba creado:\nEmail: {user.email}\nPassword: SecurePass123!")
    except Exception as e:
        print(f"❌ Error creando usuario: {str(e)}")

if __name__ == "__main__":
    asyncio.run(create_test_user())