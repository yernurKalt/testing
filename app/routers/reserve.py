import json
import re
from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
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
@inject
async def add_reservation(
    user: Annotated[User, Depends(get_current_user)],
    session: FromDishka[AsyncSession],
    reservation: ReservationBase
):
    reservation = ReservationCreate(
        is_confirmed=None,
        product_id=reservation.product_id,
        user_id=user.id
    )
    reservationService = ReservationService()
    reservation = await reservationService.create_reservation(session, reservation)
    return reservation

@router.get("/all")
@inject
async def get_all_reservations(
    user: Annotated[User, Depends(get_current_user)],
    session: FromDishka[AsyncSession]
):
    reservationService = ReservationService()
    reservations = await reservationService.get_all_reservations(session)
    return [ReservationOut.model_validate(reservation).model_dump() for reservation in reservations]

@router.get("/all_confirmed")
async def get_all_confirmed_reservations(user: Annotated[User, Depends(get_current_user)]):
    reservationService = ReservationService()
    result = await reservationService.get_all_confirmed_reservations()
    return result

@router.get("/all_cancelled")
async def get_all_confirmed_reservations(user: Annotated[User, Depends(get_current_user)]):
    reservationService = ReservationService()
    result = await reservationService.get_all_cancelled_reservations()
    return result

@router.get("/all_expired")
async def get_all_confirmed_reservations(user: Annotated[User, Depends(get_current_user)]):
    reservationService = ReservationService()
    result = await reservationService.get_all_expired_reservations()
    return result


@router.get("/get_reservation_info")
@inject
async def get_reservation(
    user: Annotated[User, Depends(get_current_user)],
    reservation_id: int,
    session: FromDishka[AsyncSession]
):
    reservationService = ReservationService()
    reservation = await reservationService.get_reservation_by_id(session, reservation_id)
    return reservation


@router.patch("/confirm")
@inject
async def confirm(
    session: FromDishka[AsyncSession],
    user: Annotated[User, Depends(get_current_user)],
    reservation_id: int,
):
    reservationService = ReservationService()
    result = await reservationService.confirm_reservation(session, reservation_id)
    return ReservationOut.model_validate(result).model_dump()

@router.delete("/cancel")
@inject
async def cancel(
    session: FromDishka[AsyncSession],
    user: Annotated[User, Depends(get_current_user)],
    reservation_id: int
):
    reservationService = ReservationService()
    await reservationService.delete_reservation(session, reservation_id)
    return {"Message": f"reservation witd id={reservation_id} was deleted"}