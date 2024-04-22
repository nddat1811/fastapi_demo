from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class NewWaterBillRequest(BaseModel):
    staff_id: int
    user_id :int
    prev_volume: int
    cur_volume: int


class WaterBillResponse(BaseModel):
    id: int
    user_id :int
    prev_volume: int
    cur_volume: int
    total_volume: int
    price: int
    due_date: datetime
    payment_date: Optional[datetime]
    total_volume_price: int
    created_at: datetime

class UpdateWaterBillRequest(BaseModel):
    prev_volume: int
    cur_volume: int
    user_id: int
    pay: Optional[bool]
    flag_delete: Optional[bool]