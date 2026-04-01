import asyncio
import json
import time
import redis.asyncio as redis

from app.db.db import async_session
from app.repositories.product import ProductRepo
from app.repositories.reservation import ReservationRepo


r = redis.Redis(host='localhost', port=6379, decode_responses=True)
productRepo = ProductRepo()
reservationRepo = ReservationRepo()


async def background_job(r):
    async with async_session() as session:
        while True:
            reservations = await r.hgetall("reservation")
            for reservation_data in reservations:
                reservation = json.loads(reservations[reservation_data])
                if time.time() > float(reservation["time"]) and not bool(reservation["is_confirmed"]):

                    await productRepo.increase_stock(session, int(reservation["product_id"]))
                    await reservationRepo.delete_reservation_by_id(session, int(reservation_data))
                    await r.hdel("reservation", reservation_data)
            await asyncio.sleep(11)

if __name__ == "__main__":
    asyncio.run(background_job(r))
