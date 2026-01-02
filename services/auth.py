import os 
from fastapi import HTTPException, Request

def ip_allowed(client_ip: str) -> bool:
    allowed = os.getenv('DEV_ALLOWED_IP')
    return client_ip == allowed

def valid_login_data(data: object) -> bool:
    correct_email = os.getenv('VALID_EMAIL')
    correct_password = os.getenv('VALID_PASSWORD')

    if data.password == correct_password and data.email == correct_email:
        return True 
    return False

async def admin_guard(request: Request):
    session = request.cookies.get('admin_session')

    if session != 'admin_logged':
        raise HTTPException(status_code=401, detail='Não autenticado')