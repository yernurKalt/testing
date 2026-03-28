from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product import ProductRepo
from app.schemas.product import ProductCreate


class ProductService:
    def __init__(self) -> None:
        self.productRepo = ProductRepo()

    async def create_new_product(self, session: AsyncSession, product: ProductCreate):
        if await self.productRepo.get_product_by_name(session, product.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product with that name already exists"
            )
        result = await self.productRepo.create_product(session, product)
        return result

    async def get_product_by_id(self, session: AsyncSession, product_id: int):
        result = await self.productRepo.get_product_by_id(session, product_id)
        if result:
            return result
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product with that id does not exist"
        )