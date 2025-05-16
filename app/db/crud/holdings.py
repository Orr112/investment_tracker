from sqlalchemy.orm import Session
from app.db.models.investment import Holding
from app.schemas.holdings import HoldingCreate, HoldingUpdate

def create_holding(db: Session, holding: HoldingCreate) -> Holding:
    db_holding = Holding(**holding.dict())
    db.add(db_holding)
    db.commit()
    db.refresh(db_holding)
    return db_holding

def get_holding(db: Session, holding_id: int) -> Holding | None:
    return db.query(Holding).filter(Holding.id == holding_id).first()

def get_all_holdings(db: Session) -> list[Holding]:
    return db.query(Holding).all()

def update_holding(db: Session, holding_id: int, update: HoldingUpdate) -> Holding | None:
    holding = get_holding(db, holding_id)
    if not holding:
        return None
    for key, value in update.dict(exclude_unset=True).items():
        setattr(holding, key, value)
        db.commit()
        db.refresh(holding)
        return holding

def delete_holding(db: Session, holding_id: int) -> bool:
    holding = get_holding(db, holding_id)
    if not holding:
        return False
    db.delete(holding)
    db.commit()
    return True