from pydantic import BaseModel

class ProductSchema(BaseModel):
    name: str 
    price: float 
    tag: str 
    slug: str
    parts: int 
    partsPrice: float
    productLink: str 
    imageUrl: str
    imagePublicId: str 
    views: int = 0
    created_at: str