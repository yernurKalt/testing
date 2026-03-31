import re
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_db
from app.models.user import User
from app.schemas.reservation import ReservationBase, ReservationCreate, ReservationOut
from app.schemas.user import UserCreate
from app.services.authenticate import get_current_user
from app.services.create_reservation import ReservationService


router = APIRouter(
    prefix="/reserve",
    tags=['reserve'],
)


@router.post("")
async def add_reservation(
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_db)],
    reservation: ReservationBase
):
    reservation = ReservationCreate(
        is_confirmed=reservation.is_confirmed,
        product_id=reservation.product_id,
        user_id=user.id
    )
    reservationService = ReservationService()
    reservation = await reservationService.create_reservation(session, reservation)
    return reservation

@router.get("/get_reservation_info")
async def get_reservation(
    user: Annotated[User, Depends(get_current_user)],
    reservation_id: int,
    session: Annotated[AsyncSession, Depends(get_db)]
):
    reservationService = ReservationService()
    reservation = await reservationService.get_reservation(session, reservation_id)
    return reservation


@router.patch("/confirm")
async def confirm(
    session: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    reservation_id: int,
):
    reservationService = ReservationService()
    result = await reservationService.confirm_reservation(session, reservation_id)
    return ReservationOut.model_validate(result).model_dump()