from fastapi import Depends
from app.database import get_db
from app.services.auth_service import AuthService

# Dependency to get the database object
def get_auth_service(db = Depends(get_db)):
    return AuthService(db)

# Uso típico en un endpoint:
# async def my_endpoint(db: Database = Depends(get_database)):