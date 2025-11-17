from fastapi import HTTPException
from app.auth_module.sessions import SessionDataDep

async def get_current_user(session_data: SessionDataDep) -> str:
    "Проверка авторизации пользователяи возвращение логина пользователя"
    if not session_data or not session_data.login:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return session_data.login