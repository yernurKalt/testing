import asyncio

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import async_session
from app.repositories.product import ProductRepo
from app.repositories.reservation import ReservationRepo
from app.repositories.user import UserRepo
from app.schemas.reservation import ReservationCreate
from app.services.sched.routers.reserve import check_reservation_status


class ReservationService:
    def __init__(self):
        self.userRepo = UserRepo()
        self.reservationRepo = ReservationRepo()
        self.productRepo = ProductRepo()
        self.TTL_SECONDS = 10

    async def _expire_reservation(self, session: AsyncSession, reservation_id: int) -> None:
        await asyncio.sleep(self.TTL_SECONDS)
        
        db_reservation = await self.reservationRepo.get_reservation_by_id(session, reservation_id)
        if db_reservation is None:
            return

        if db_reservation.is_confirmed:
            return

        await self.productRepo.increase_stock(session, db_reservation.product_id)
        await self.reservationRepo.delete_reservation_by_id(session, reservation_id)

    async def create_reservation(self, session: AsyncSession, reservation: ReservationCreate):
        product = await self.productRepo.get_product_by_id(session, reservation.product_id)
        if product.stock < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product ran out of stock"
            )
        await self.productRepo.decrease_stock(session, reservation.product_id)
        result = await self.reservationRepo.create_reservation(session, reservation)
        job = await check_reservation_status.schedule(result.id).delay(10)

        return result

    async def get_reservation(self, session: AsyncSession, reservation_id: int):
        
        db_reservation = await self.reservationRepo.get_reservation_by_id(
            session,
            reservation_id,
            )
        if db_reservation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"reservation with id {reservation_id} not found",
            )
        return db_reservation

    async def confirm_reservation(self, session: AsyncSession, reservation_id: int):
        db_reservation = await self.reservationRepo.confirm_reservation(session, reservation_id)
        if db_reservation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"reservation with id {reservation_id} not found",
            )
        return db_reservation