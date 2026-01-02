from fastapi import APIRouter, Request, Response, HTTPException, Depends
from services.auth import ip_allowed, admin_guard, valid_login_data
from models.login import LoginSchema

product_list_test = [
    {
        'id': 0,
        'name': 'Smart TV 32 Philco Led',
        'price': 889.0,
        'price_card': '18x R$ 94.88',
        'tag': 'TVs',
        'image': '',
        'description': ''
    },
    {
        'id': 1,
        'name': 'Celular',
        'price': 1400.0,
        'price_card': '10x R$ 140',
        'tag': 'Celulares',
        'image': '',
        'description': ''
    },
    {
        'id': 2,
        'name': 'Celular',
        'price': 1800.0,
        'price_card': '10x R$ 180',
        'tag': 'Celulares',
        'image': '',
        'description': ''
    }
]

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

@router.delete('/products/{product_id}')
async def delete_product(product_id: int , _: None = Depends(admin_guard)): # Mudar de int para str quando for gerar os ids do jeito certo
    print(product_id)
    for p in product_list_test:
        if p['id'] == product_id:
            index = product_list_test.index(p)
            del product_list_test[index]

    return {'ok': True}
