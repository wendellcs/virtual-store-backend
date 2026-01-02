from fastapi import APIRouter, Request, Response, HTTPException, Depends
from services.auth import ip_allowed, admin_guard, valid_login_data
from models.login import LoginSchema

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)

@router.get('/access')
async def access_to_dashboard(_: None = Depends(admin_guard)):
    return {'dados': 'somente admin'}

@router.post('/login')
async def admin_login(data: LoginSchema, request: Request, response: Response):
    if not ip_allowed(request.client.host):
        raise HTTPException(status_code=403, detail="IP não autorizado")
    
    if not valid_login_data(data):
        raise HTTPException( status_code=401, detail="Acesso negado")
    
    response.set_cookie(
        key='admin_session',
        value='admin_logged', # Mudar para token
        httponly=True,
        secure=False, # Em produção, mudar para true.
        samesite='lax',
        max_age= 60 * 60 # 1 hora
    )

    return {'ok': True}

@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('admin_session')
    return {'ok': True}

