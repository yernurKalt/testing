from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str

class ProductCreate(ProductBase):
    initialStock: int = 0

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    stock: Optional[int] = None

class ProductOut(ProductBase):
    id: int
    stock: int
    model_config = ConfigDict(from_attributes=True)