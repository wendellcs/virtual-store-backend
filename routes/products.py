from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends, Query
from math import ceil
import cloudinary.uploader
from services.auth import admin_guard
from database.mongo import collection
from bson.objectid import ObjectId
from datetime import date

router = APIRouter(
    prefix='/products',
    tags=['Products']
)

def serialize_mongo(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@router.get('')
async def get_products(
    page: int = Query (1 , ge = 1),
    limit: int = Query (10, ge = 1 , le = 100)
):
    skip = (page - 1) * limit

    products = list(collection.find().skip(skip).limit(limit))
    products = [serialize_mongo(p) for p in products]

    total = collection.count_documents({})

    return {
        'page': page,
        'limit': limit,
        'total': total,
        'pages': ceil(total / 12),
        'data': products
    }

@router.get("/search")
def search_products(
    q: str = Query(..., min_length=2),
    page: int = Query(1 , ge = 1),
    limit: int = Query(10, ge = 1, le = 100)
):
    skip = (page - 1) * limit

    products = collection.find({
        "name": {
            "$regex": q,
            "$options": "i"
        }
    }).skip(skip).limit(limit)

    products = [serialize_mongo(p) for p in products]

    return {
        'page': page,
        'limit': limit,
        'pages': ceil(len(products) / 12),
        'data': products
    }

@router.post('')
async def create_product(
    name: str = Form(...), 
    tag: str = Form(...),
    price: float = Form(...),
    parts: int = Form(...),
    partsPrice: float = Form(...),
    productLink: str = Form(...),
    image: UploadFile = File(...)
):
    
    print('Parte 1 OKAY')
    if not image.content_type.startswith('image/'):
        raise HTTPException(400, 'Apenas imagens')

    result = cloudinary.uploader.upload(image.file, folder = 'produtos')

    print('Parte 2 OKAY', result)

    product = {
        'name': name,
        'tag': tag,
        'price': price,
        'parts': parts,
        'partsPrice': partsPrice,
        'productLink': productLink,
        'imageUrl': result['secure_url'],
        'imagePublicId': result['public_id'],
        'views': 0,
        'created_at': str(date.today())
    }
    print(product)
    collection.insert_one(product)

    print('Ultima parte ---------')


    return {'ok': True}

@router.delete('/{product_id}')
async def delete_product(product_id: str , _: None = Depends(admin_guard)): 
    # Mudar para find_one
    productPublicId = collection.find({}, {'imagePublicId':1,'_id': ObjectId(product_id)})[0]['imagePublicId']
    cloudinary.uploader.destroy(productPublicId)
    collection.delete_one({'_id': ObjectId(product_id)})
    return {'ok': True}
