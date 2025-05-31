from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.investment import InvestmentPosition
from app.schemas.holdings import HoldingCreate, HoldingUpdate
from typing import List
import logging

logger = logging.getLogger(__name__)

def create_holding(db: Session, holding: HoldingCreate) -> InvestmentPosition:
    data = holding.dict()
    data["shares"] = data.pop("quantity")
    db_holding = InvestmentPosition(**data)
    db.add(db_holding)
    db.commit()
    db.refresh(db_holding)
    return db_holding

def get_holding(db: Session, holding_id: int) -> InvestmentPosition | None:
    return db.query(InvestmentPosition).filter(InvestmentPosition.id == holding_id).first()

def get_all_holdings(db: Session) -> list[InvestmentPosition]:
    return db.query(InvestmentPosition).all()

def list_holdings(db: Session) -> List[InvestmentPosition]:
    return db.query(InvestmentPosition).all()

def update_holding(db: Session, holding_id: int, holding_update: HoldingUpdate):
    db_holding = db.query(InvestmentPosition).get(holding_id)
    if not db_holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    for field, value in holding_update.dict(exclude_unset=True).items():
        logger.debug(f"Updating field {field} to {value}")
        setattr(db_holding, field, value)
    db.commit()
    db.refresh(db_holding)
    return db_holding

def delete_holding(db: Session, holding_id: int):
    db_holding = db.query(InvestmentPosition).get(holding_id)
    if not db_holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    db.delete(db_holding)
    db.commit()
    return {"deleted": True}