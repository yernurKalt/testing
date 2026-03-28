from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product import ProductRepo
from app.repositories.reservation import ReservationRepo
from app.repositories.user import UserRepo
from app.schemas.reservation import ReservationBase


class ReservationService:
    def __init__(self):
        self.userRepo = UserRepo()
        self.reservationRepo = ReservationRepo()
        self.productRepo = ProductRepo()

    async def create_reservation(self, session: AsyncSession, reservation: ReservationBase):
        if reservation.is_confirmed is None or reservation.is_confirmed == True:
            product = await self.productRepo.decrease_stock(session, reservation.product_id)
            print(product)
        result = await self.reservationRepo.create_reservation(session, reservation)
        return result
