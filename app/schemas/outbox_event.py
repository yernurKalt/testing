from pydantic import BaseModel, ConfigDict

class OutboxEventOut(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)