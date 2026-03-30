from typing import Optional
from pydantic import BaseModel, ConfigDict

class ReservationBase(BaseModel):
    is_confirmed: bool = False
    product_id: int

class ReservationCreate(ReservationBase):
    user_id: int


class ReservationOut(ReservationCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)