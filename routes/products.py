from fastapi import APIRouter, UploadFile, File, HTTPException, Form
import cloudinary.uploader
from database.mongo import collection, db

router = APIRouter(
    prefix='/products',
    tags=['Products']
)

def serialize_mongo(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@router.get('/')
async def get_products():
    products = list(collection.find())
    products = [serialize_mongo(p) for p in products]
    return products

@router.get('/{product_id}')
def get_product(product_id: int) -> dict:
    return {'product': 'example'}

@router.post('/')
async def create_product(
    name: str = Form(...), 
    description: str = Form(...), 
    tag: str = Form(...),
    price: float = Form(...),
    parts: int = Form(...),
    partsPrice: float = Form(...),
    productLink: str = Form(...),
    image: UploadFile = File(...)
):
    if not image.content_type.startswith('image/'):
        raise HTTPException(400, 'Apenas imagens')

    result = cloudinary.uploader.upload(image.file, folder = 'produtos')

    product = {
        'name': name,
        'description': description,
        'tag': tag,
        'price': price,
        'parts': parts,
        'partsPrice': partsPrice,
        'productLink': productLink,
        'imageUrl': result['secure_url']
    }

    collection.insert_one(product)

    return {'ok': True}

