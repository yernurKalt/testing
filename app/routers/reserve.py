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
    session: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    reservation: ReservationBase
):
    reservation = ReservationCreate(
        is_confirmed=reservation.is_confirmed,
        product_id=reservation.product_id,
        user_id=user.id
    )
    reservationService = ReservationService()
    reservation = await reservationService.create_reservation(session, reservation)
    return ReservationOut.model_validate(reservation).model_dump()