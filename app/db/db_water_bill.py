from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..auth import oauth2
from app.models.user import DbUser
from app.schemas.authentication import AuthResponse, RegistrationRequest
from app.schemas.water_bill import NewWaterBillRequest, UpdateWaterBillRequest
from app.utils.calc import calculate_price
from app.utils.constants import Role
from . import hash
from datetime import timedelta, datetime
from app.models import DbWaterBill
from . import db_user
from sqlalchemy import text


async def get_water_bill_by_id(id: int, db: Session):
    bill_water = db.query(DbWaterBill).filter(DbWaterBill.id == id, DbWaterBill.deleted_at == None).first()
    if not bill_water:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bill water with id: {id} not found")
    return bill_water

async def create_water_bill(req: NewWaterBillRequest, user: DbUser, db: Session):
    user = await db_user.get_user_by_id(db, req.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {req.user_id} not found")
    if req.cur_volume < req.prev_volume:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Current volume must be greater than previous volume")
    bill_water = DbWaterBill(
        user_id = req.user_id,
        prev_volume = req.prev_volume,
        cur_volume = req.cur_volume,
    )
    bill_water.created_by = user.id
    bill_water.total_volume = req.cur_volume - req.prev_volume
    bill_water.price = calculate_price(bill_water.total_volume)
    bill_water.total_volume_price = bill_water.price * bill_water.total_volume
    bill_water.due_date = datetime.now() + timedelta(days=14)
    db.add(bill_water)
    db.commit()
    db.refresh(bill_water)
    return bill_water

async def update_water_bill(req: UpdateWaterBillRequest, id:int,  db: Session):
    bill_water =  await get_water_bill_by_id(id, db)
    if not bill_water:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bill water with id: {id} not found")
    if req.cur_volume < req.prev_volume:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Current volume must be greater than previous volume")
    bill_water.prev_volume = req.prev_volume
    bill_water.cur_volume = req.cur_volume
    bill_water.total_volume = req.cur_volume - req.prev_volume
    bill_water.price = calculate_price(bill_water.total_volume)
    bill_water.total_volume_price = bill_water.price * bill_water.total_volume
    user = await db_user.get_user_by_id(db, req.user_id)
    bill_water.user_id = req.user_id

    if req.pay == True:
        bill_water.payment_date = datetime.now()
    elif req.flag_delete == True:
        bill_water.deleted_at = datetime.now()

    db.commit()
    return bill_water

async def get_list_water_bill(db:Session):
    bills = db.query(DbWaterBill).order_by(desc(DbWaterBill.created_at)).all()
    if len(bills) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid query ')
    return bills

async def get_list_water_bill_by_user_id(user_id:int, db:Session):
    bills = db.query(DbWaterBill).filter(DbWaterBill.user_id == user_id, DbWaterBill.deleted_at == None).order_by(desc(DbWaterBill.created_at)).all()
    if len(bills) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Invalid query with user_id {user_id}')
    return bills

async def get_water_bill_in_month(p_month: int, db: Session):
    # execute stored procedure
    stmt = text("CALL WaterBillInMonth(:p_month, 'rs_resultone')")
    db.execute(stmt, {'p_month': p_month})
    results = db.execute(text("FETCH ALL FROM rs_resultone"))
    # parse the results into a list
    bills = []
    for row in results:
        try:
            # Can unpacking the results then create bill dicts or use rows
            # username, prev_volume, cur_volume, total_volume, price, total_volume_price, due_date, payment_date,created_date = row
            bill_dict = {
                "username": row[0],
                "prev_volume": row[1],
                "cur_volume": row[2],
                "total_volume": row[3],
                "price": row[4],
                "total_volume_price": row[5],
                "due_date": row[6],
                "payment_date": row[7],
                "created_date": row[8],
                "creator": row[9],
            }
            bills.append(bill_dict)
        except ValueError as e:
            print(f"Error processing row: {e}")

    return bills