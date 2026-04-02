import asyncio
import json
import time

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import async_session
from app.repositories.ioc import repos_container
from app.repositories.product import ProductRepo
from app.repositories.reservation import ReservationRepo
from app.repositories.user import UserRepo
from app.schemas.reservation import ReservationCreate
from app.services.redis.main import r


class ReservationService:
    def __init__(self):
        self.TTL_SECONDS = 10 #code will be improved via dishka in the future 


    async def create_reservation(self, session: AsyncSession, reservation: ReservationCreate):
        reservationRepo = await repos_container.get(ReservationRepo)
        productRepo = await repos_container.get(ProductRepo)
        product = await productRepo.get_product_by_id(session, reservation.product_id)
        if product.stock < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product ran out of stock"
            )
        await productRepo.decrease_stock(session, reservation.product_id)
        result = await reservationRepo.create_reservation(session, reservation)
        #job = await check_reservation_status.schedule(result.id).delay(10)
        await r.hset(
            "reservation",
            str(result.id),
            json.dumps(
                {
                    "time": time.time() + self.TTL_SECONDS,
                    "product_id": result.product_id,
                    "is_confirmed": result.is_confirmed,
                }
            )
        )
        return result
 
    async def get_reservation(self, session: AsyncSession, reservation_id: int):
        reservationRepo = await repos_container.get(ReservationRepo)
        db_reservation = await reservationRepo.get_reservation_by_id(
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
        reservationRepo = await repos_container.get(ReservationRepo)
        db_reservation = await reservationRepo.confirm_reservation(session, reservation_id)
        await r.hset(
            "reservation",
            str(db_reservation.id),
            json.dumps(
                {
                    "time": time.time() + self.TTL_SECONDS,
                    "product_id": db_reservation.product_id,
                    "is_confirmed": db_reservation.is_confirmed,
                }
            )
        )
        if db_reservation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"reservation with id {reservation_id} not found",
            )
        return db_reservation