from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.ioc import repos_container
from app.repositories.product import ProductRepo
from app.schemas.product import ProductCreate, ProductUpdate


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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product with that id does not exist"
        )

    async def get_all_products(self, session: AsyncSession):
        productRepo = await repos_container.get(ProductRepo)
        return await productRepo.get_all_products(session)

    async def update_product(
        self, session: AsyncSession, product_id: int, update: ProductUpdate
    ):
        productRepo = await repos_container.get(ProductRepo)
        if update.name is not None:
            existing = await productRepo.get_product_by_name(session, update.name)
            if existing and existing.id != product_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Product with that name already exists",
                )
        result = await productRepo.update_product(session, product_id, update)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product with that id does not exist",
            )
        return result

    async def delete_product(self, session: AsyncSession, product_id: int):
        productRepo = await repos_container.get(ProductRepo)
        deleted = await productRepo.delete_product(session, product_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product with that id does not exist",
            )
        return {"message": f"product with id={product_id} was deleted"}