from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.holdings import HoldingCreate, HoldingUpdate, HoldingOut
from app.db import crud

router = APIRouter(prefix="/holdings", tags=["Holdings"])

@router.post("/", response_model=HoldingOut)
def create_holding(holding: HoldingCreate, db: Session = Depends(get_db)):
    return crud.create_holding(db, holding)

@router.get("/{holding_id}", response_model=HoldingOut)
def get_holding(holding_id: int, db: Session = Depends(get_db)):
    db_holding = crud.get_holding(db=db, holding_id=holding_id)
    if db_holding is None:
        raise HTTPException(status_code=404, detail="Holding not found")
    return db_holding

@router.get("/", response_model=List[HoldingOut])
def list_holdings(db: Session = Depends(get_db)):
    return crud.list_holdings(db=db)

@router.post("/{holding_id}", response_model=HoldingOut)
def update_holding(holding_id: int, update: HoldingUpdate,  db: Session = Depends(get_db)):
    db_holding = crud.update_holding(db=db, holding_id=holding_id, update=update)
    if db_holding is None:
        raise HTTPException(statu_code=404, detail="Holding not found")
    return db_holding 