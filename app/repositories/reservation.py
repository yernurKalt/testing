from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reservation import ReservationModel
from app.schemas.reservation import ReservationBase


class ReservationRepo:
    def __init__(self) -> None:
        pass

    async def create_reservation(self, session: AsyncSession, reservation: ReservationBase):
        newReservation = ReservationModel(
            is_confirmed=reservation.is_confirmed,
            user_id=reservation.user_id,
            product_id=reservation.product_id,
        )
        session.add(newReservation)
        await session.commit()
        return newReservation