from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.ioc import repos_container
from app.repositories.product import ProductRepo
from app.schemas.product import ProductCreate


class ProductService:

    async def create_new_product(self, session: AsyncSession, product: ProductCreate):
        productRepo = await repos_container.get(ProductRepo)
        if await productRepo.get_product_by_name(session, product.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product with that name already exists"
            )
        result = await productRepo.create_product(session, product)
        return result

    async def get_product_by_id(self, session: AsyncSession, product_id: int):
        productRepo = await repos_container.get(ProductRepo)
        result = await productRepo.get_product_by_id(session, product_id)
        if result:
            return result
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product with that id does not exist"
        )