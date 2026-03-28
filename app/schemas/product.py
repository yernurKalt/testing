from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str

class ProductCreate(ProductBase):
    initialStock: int = 0

class ProductOut(ProductBase):
    id: int
    stock: int
    model_config = ConfigDict(from_attributes=True)