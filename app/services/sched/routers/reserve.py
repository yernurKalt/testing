from typing import Annotated
from fastapi import Depends
from jobify import JobRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import async_session, get_db
from app.repositories.product import ProductRepo
from app.repositories.reservation import ReservationRepo


router = JobRouter()
reservationRepo = ReservationRepo()
productRepo = ProductRepo()

@router.task
async def check_reservation_status(
    reservation_id: int,
):
    async with async_session() as session:
        db_reservation = await reservationRepo.get_reservation_by_id(session, reservation_id)
        if db_reservation is None:
            return

        if db_reservation.is_confirmed:
            return

        await productRepo.increase_stock(session, db_reservation.product_id)
        await reservationRepo.delete_reservation_by_id(session, reservation_id)