import asyncio

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product import ProductRepo
from app.repositories.reservation import ReservationRepo
from app.repositories.user import UserRepo
from app.schemas.reservation import ReservationBase, ReservationCreate


class ReservationService:
    def __init__(self):
        self.userRepo = UserRepo()
        self.reservationRepo = ReservationRepo()
        self.productRepo = ProductRepo()
        self.TTL = 20


    async def create_reservation(self, session: AsyncSession, reservation: ReservationCreate):
        pass

    async def get_reservation(self, reservation: ReservationCreate):
        pass
    async def confirm_reservation(self, session: AsyncSession, reservation: ReservationCreate):
        pass