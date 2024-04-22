from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.user import DbUser
from app.schemas.authentication import AuthResponse, RegistrationRequest
from app.schemas.water_bill import NewWaterBillRequest, UpdateWaterBillRequest
from app.utils.calc import calculate_price
from app.utils.constants import Role
from . import hash, oauth2
from datetime import timedelta, datetime
from app.models import DbWaterBill
from . import db_user


async def get_water_bill_by_id(id: int, db: Session):
    bill_water = db.query(DbWaterBill).filter(DbWaterBill.id == id).first()
    if not bill_water:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bill water with id: {id} not found")
    return bill_water

# async def get_last_volume(user_id:int,  db: Session):
#     bill_water = db.query(DbWaterBill).filter(DbWaterBill.user_id == user_id).order_by(desc(DbWaterBill.created_at)).first()
#     if not bill_water:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bill water with id: {id} not found")
#     return bill_water


# Chưa có get current user --> staff id test tạm
async def create_water_bill(req: NewWaterBillRequest, db: Session):
    user = db_user.get_user_by_id(db, req.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {req.user_id} not found")
    staff = db.query(DbUser).filter(DbUser.id == req.staff_id).first()
    if staff.role != Role.STAFF:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id: {req.user_id} is not staff")

    bill_water = DbWaterBill(
        user_id = req.user_id,
        prev_volume = req.prev_volume,
        cur_volume = req.cur_volume,
    )
    bill_water.total_volume = req.cur_volume - req.prev_volume
    bill_water.price = calculate_price(bill_water.total_volume)
    bill_water.total_volume_price = bill_water.price * bill_water.total_volume
    bill_water.due_date = datetime.now() + timedelta(days=14)
    db.add(bill_water)
    db.commit()
    db.refresh(bill_water)
    return bill_water

async def update_water_bill(req: UpdateWaterBillRequest, id:int,  db: Session):
    bill_water = db.query(DbWaterBill).filter(DbWaterBill.id == id).first()
    if not bill_water:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bill water with id: {req.id} not found")
    bill_water.prev_volume = req.prev_volume
    bill_water.cur_volume = req.cur_volume
    bill_water.total_volume = req.cur_volume - req.prev_volume
    bill_water.price = calculate_price(bill_water.total_volume)
    bill_water.total_volume_price = bill_water.price * bill_water.total_volume
    user = db_user.get_user_by_id(db, req.user_id)
    bill_water.user_id = req.user_id

    if req.pay == True:
        bill_water.payment_date = datetime.now()
    elif req.flag_delete == True:
        bill_water.deleted_at = datetime.now()

    db.commit()
    return bill_water

async def get_list_water_bill(db:Session):
    bills = db.query(DbWaterBill).order_by(desc(DbWaterBill.created_at)).all()
    return bills

async def get_list_water_bill_by_user_id(user_id:int, db:Session):
    bills = db.query(DbWaterBill).filter(DbWaterBill.user_id == user_id).order_by(desc(DbWaterBill.created_at)).all()
    return bills