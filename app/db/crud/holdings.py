from sqlalchemy.orm import Session
from app.db.models.investment import InvestmentPosition
from app.schemas.holdings import HoldingCreate, HoldingUpdate

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

def update_holding(db: Session, holding_id: int, update: HoldingUpdate) -> InvestmentPosition | None:
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