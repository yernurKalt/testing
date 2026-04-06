import asyncio
import json
import time
import redis.asyncio as redis

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import async_session
from app.repositories.ioc import repos_container
from app.repositories.product import ProductRepo
from app.repositories.reservation import ReservationRepo
from app.repositories.user import UserRepo
from app.schemas.reservation import ReservationCreate
from app.services.redis.main import r, redisContainer



class ReservationService:
    def __init__(self):
        self.TTL_SECONDS = 15 #code will be improved via dishka in the future 


    async def create_reservation(self, session: AsyncSession, reservation: ReservationCreate):
        reservationRepo = await repos_container.get(ReservationRepo)
        productRepo = await repos_container.get(ProductRepo)
        if await self.get_reservation_by_product_and_user_id(
            session,
            reservation.product_id,
            reservation.user_id,
        ):
            
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"reservation with user id={reservation.user_id} and product id={reservation.product_id} already exists"
            )
        product = await productRepo.get_product_by_id(session, reservation.product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product is not found"
            )
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
                    "is_confirmed": None,
                }
            )
        )
        return result
    
    async def get_all_reservations(
        self,
        session: AsyncSession
    ):
        reservationRepo = await repos_container.get(ReservationRepo)
        return await reservationRepo.get_all_reservations(session)

    async def get_all_confirmed_reservations(self):
        r = await redisContainer.get(redis.Redis)
        all_confirmed_reserevations = await r.hgetall("confirmed_reservations")
        for res in all_confirmed_reserevations:
            all_confirmed_reserevations[res] = json.loads(all_confirmed_reserevations[res])
        return all_confirmed_reserevations

    async def get_all_cancelled_reservations(self):
        r = await redisContainer.get(redis.Redis)
        all_cancelled_reserevations = await r.hgetall("cancelled_reservations")
        for res in all_cancelled_reserevations:
            all_cancelled_reserevations[res] = json.loads(all_cancelled_reserevations[res])
        return all_cancelled_reserevations

    async def get_all_expired_reservations(self):
        r = await redisContainer.get(redis.Redis)
        all_expired_reserevations = await r.hgetall("expired_reservation")
        for res in all_expired_reserevations:
            all_expired_reserevations[res] = json.loads(all_expired_reserevations[res])
        return all_expired_reserevations

    async def get_reservation_by_id(self, session: AsyncSession, reservation_id: int):
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

    async def get_reservation_by_product_and_user_id(
        self,
        session: AsyncSession,
        product_id: int,
        user_id: int,
    ):
        reservationRepo = await repos_container.get(ReservationRepo)
        db_reservation = await reservationRepo.get_reservation_by_product_and_user_id(
            session,
            product_id,
            user_id,
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
                    "is_confirmed": True,
                }
            )
        )
        if db_reservation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"reservation with id {reservation_id} not found",
            )
        return db_reservation

    async def delete_reservation(
        self,
        session: AsyncSession,
        reservation_id: int
    ): 
        reservationRepo = await repos_container.get(ReservationRepo)
        productRepo = await repos_container.get(ProductRepo)
        deleted_reservation = await reservationRepo.get_reservation_by_id(session, reservation_id)
        if deleted_reservation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="such reervation does not exist"
            )
        await productRepo.increase_stock(session, deleted_reservation.product_id)
        await r.hset(
            "reservation",
            str(deleted_reservation.id),
            json.dumps(
                {
                    "time": time.time() + self.TTL_SECONDS,
                    "product_id": deleted_reservation.product_id,
                    "is_confirmed": False,
                }
            )
        )
        await reservationRepo.delete_reservation_by_id(
            session,
            reservation_id
        )