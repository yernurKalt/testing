from typing import Optional
from pydantic import BaseModel, ConfigDict

class ReservationBase(BaseModel):
    product_id: int

class ReservationCreate(ReservationBase):
    is_confirmed: Optional[bool] = None
    user_id: int


class ReservationOut(ReservationCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)