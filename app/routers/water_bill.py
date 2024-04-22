from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import db_water_bill
from app.schemas.water_bill import NewWaterBillRequest, WaterBillResponse, UpdateWaterBillRequest

router = APIRouter(
    prefix='/water-bills',
    tags=['water-bills']
)

@router.post('/new')
async def create_new_water_bills(req: NewWaterBillRequest, db:Session = Depends(get_db)):
    water_bill = await db_water_bill.create_water_bill(req, db)
    return water_bill


@router.get('/list-bill', response_model = List[WaterBillResponse])
async def list_water_bill(db: Session = Depends(get_db)):
    bills = await db_water_bill.list_water_bill(db)
    return bills

@router.get('/user-bills/{user_id}', response_model = List[WaterBillResponse])
async def list_user_water_bill(user_id: int, db: Session = Depends(get_db)):
    bills = await db_water_bill.get_list_water_bill_by_user_id(user_id, db)
    return bills

@router.get('/detail/{id}', response_model=WaterBillResponse)
async def get_list_water_bill_by_id(id: int, db: Session = Depends(get_db)):
    bill = await db_water_bill.get_water_bill_by_id(id, db)
    return bill

@router.put('/update/{id}', response_model=WaterBillResponse)
async def update_bill_water(req: UpdateWaterBillRequest, id: int, db: Session = Depends(get_db)):
    bill = await db_water_bill.update_water_bill(req, id, db)
    return bill
