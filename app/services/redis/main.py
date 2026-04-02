import asyncio
import json
import time
from dishka import Provider, Scope, make_async_container, provide
import redis.asyncio as redis

from app.db.db import async_session
from app.repositories.ioc import repos_container
from app.repositories.product import ProductRepo
from app.repositories.reservation import ReservationRepo


r = redis.Redis(host='localhost', port=6379, decode_responses=True)

class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    async def redis(self) -> redis.Redis:
        return r

redisContainer = make_async_container(RedisProvider())


async def background_job(r):
    productRepo = await repos_container.get(ProductRepo)
    reservationRepo = await repos_container.get(ReservationRepo)
    async with async_session() as session:
        while True:
            reservations = await r.hgetall("reservation")
            for reservation_data in reservations:
                reservation = json.loads(reservations[reservation_data])
                if time.time() > float(reservation["time"]) and (reservation["is_confirmed"]) is None:

                    await productRepo.increase_stock(session, int(reservation["product_id"]))
                    await reservationRepo.delete_reservation_by_id(session, int(reservation_data))
                    await r.hset(
                        "expired_reservation",
                        str(reservation_data),
                        json.dumps(
                            {
                                "is_confirmed": None
                            }
                        )
                    )
                    await r.hdel("reservation", reservation_data)
                elif (reservation["is_confirmed"]):
                    await r.hset(
                        "confirmed_reservations",
                        str(reservation_data),
                        json.dumps(
                            {
                                "is_confirmed": True
                            }
                        )
                    )
                    await r.hdel("reservation", reservation_data)
                elif (reservation["is_confirmed"]) == False:
                    await r.hset(
                        "cancelled_reservations",
                        str(reservation_data),
                        json.dumps(
                            {
                                "is_confirmed": False
                            }
                        )
                    )
                    await r.hdel("reservation", reservation_data)

            await asyncio.sleep(11)

if __name__ == "__main__":
    asyncio.run(background_job(r))
