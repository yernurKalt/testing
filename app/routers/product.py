from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_db
from app.models.user import User
from app.schemas.product import ProductCreate, ProductOut
from app.services.authenticate import get_current_user
from app.services.product import ProductService


router = APIRouter(
    prefix="/products",
    tags=["products"]
)
productService = ProductService()

@router.post("/") 
@inject
async def create_new_product(
    session: FromDishka[AsyncSession],
    product: ProductCreate,
    current_user: Annotated[User, Depends(get_current_user)],
) -> ProductOut:
    product = await productService.create_new_product(session, product)
    return ProductOut.model_validate(product).model_dump() 

@router.get("/")
@inject
async def get_product_by_id(
    session: FromDishka[AsyncSession],
    product_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    product = await productService.get_product_by_id(session, product_id)
    return ProductOut.model_validate(product).model_dump()