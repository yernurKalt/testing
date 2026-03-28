from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate


class ProductRepo:
    def __init__(self) -> None:
        pass
    async def create_product(self, session: AsyncSession, product: ProductCreate):
        product = Product(
            name=product.name,
            stock=product.initialStock,
        )
        session.add(product)
        await session.commit()
        result = await self.get_product_by_name(session, product.name)
        return result


    async def get_product_by_id(self, session: AsyncSession, product_id: int) -> Product:
        stmt = select(Product).where(Product.id == product_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_product_by_name(self, session: AsyncSession, name: str) -> Product:
        stmt = select(Product).where(Product.name == name)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def decrease_stock(self, session: AsyncSession, product_id: int):
        product = await self.get_product_by_id(session, product_id)
        product.stock -= 1
        await session.commit()
        return product