from dishka import make_async_container

from app.repositories.product import ProductRepoProvider
from app.repositories.reservation import ReservationRepoProvider
from app.repositories.user import UserRepoProvider

repos_container = make_async_container(
    UserRepoProvider(),
    ProductRepoProvider(),
    ReservationRepoProvider(),
)