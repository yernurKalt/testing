from dishka import Provider, Scope, provide
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reservation import ReservationModel
from app.models.user import User
from app.schemas.reservation import ReservationCreate
from app.models.product import Product


class ReservationRepo:
    def __init__(self) -> None:
        pass

    async def create_reservation(self, session: AsyncSession, reservation: ReservationCreate):
        newReservation = ReservationModel(
            is_confirmed=reservation.is_confirmed,
            user_id=reservation.user_id,
            product_id=reservation.product_id,
        )
        session.add(newReservation)
        await session.commit()
        return newReservation

    async def get_reservation_by_id(self, session: AsyncSession, reservation_id: int) -> ReservationModel | None:
        stmt = select(ReservationModel).where(ReservationModel.id == reservation_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_reservation_by_product_and_user_id(
        self,
        session: AsyncSession,
        product_id: int,
        user_id: int,
    ):
        stmt = select(ReservationModel).where(ReservationModel.product_id == product_id, ReservationModel.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def confirm_reservation(
        self, session: AsyncSession, reservation_id: int
    ) -> ReservationModel | None:
        stmt = select(ReservationModel).where(
            ReservationModel.id == reservation_id
        )
        result = await session.execute(stmt)
        db_reservation = result.scalar_one_or_none()
        if db_reservation is None:
            return None

        db_reservation.is_confirmed = True
        await session.commit()
        await session.refresh(db_reservation)
        return db_reservation

    async def delete_reservation_by_id(self, session: AsyncSession, reservation_id: int) -> None:
        stmt = select(ReservationModel).where(ReservationModel.id == reservation_id)
        result = await session.execute(stmt)
        db_reservation = result.scalar_one_or_none()
        if db_reservation is None:
            return

        await session.delete(db_reservation)
        await session.commit()
    


class ReservationRepoProvider(Provider):
    repo = provide(ReservationRepo, scope=Scope.APP)