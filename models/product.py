from pydantic import BaseModel

class Product(BaseModel):
    product_name: str 
    product_price: float 
    product_tag: str 
    product_image_url: str