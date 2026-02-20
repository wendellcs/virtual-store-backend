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

@router.get('/top_products')
async def get_top_products():
    top_products = collection.find().sort('views', -1).limit(8)
    top_products = [serialize_mongo(p) for p in top_products]
    return top_products

@router.get("/search")
async def search_products(
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

@router.get('/{product_id}')
async def get_product_by_id(product_id: str):
    product = collection.find_one({'_id': ObjectId(product_id)})
    product = serialize_mongo(product)
    return product

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
    if not image.content_type.startswith('image/'):
        raise HTTPException(400, 'Apenas imagens')

    result = cloudinary.uploader.upload(image.file, folder = 'produtos')

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
    collection.insert_one(product)
    return {'ok': True}

@router.patch('/{product_id}/view')
async def update_view(product_id: str):
    collection.update_one(
        {'_id': ObjectId(product_id)},
        {'$inc':{'views': 1}})
    
    return {'ok': True}

@router.delete('/{product_id}')
async def delete_product(product_id: str , _: None = Depends(admin_guard)): 
    # Mudar para find_one
    productPublicId = collection.find({}, {'imagePublicId':1,'_id': ObjectId(product_id)})[0]['imagePublicId']
    cloudinary.uploader.destroy(productPublicId)
    collection.delete_one({'_id': ObjectId(product_id)})
    return {'message': 'Produto removido!'}
