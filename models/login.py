from pydantic import BaseModel, Field

class LoginSchema(BaseModel):
    email: str 
    password: str = Field(min_length = 8)