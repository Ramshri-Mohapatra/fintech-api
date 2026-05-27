from fastapi import APIRouter, Depends, HTTPException , status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(tags=["Transaction"])

@router.post("/transactions", response_model = schemas.TransactionResponse, status_code = status.HTTP_201_CREATED)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    new_transaction = models.Transaction(amount = transaction.amount, category= transaction.category, description = transaction.description, type = transaction.type, user_id = current_user.id)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@router.get("/transactions", response_model = List[schemas.TransactionResponse])
def get_transactions(category: Optional[str] = None, type: Optional[str] = None, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = db.query(model.Transaction).filter(models.Transaction.user_id == current_user.id)

    if category:
        query = query.filterr(models.Transaction.category == category )
    if type:
        query = query.filter(models.Transaction.type == type)

    return query.all()

@router.get("/transactions/{transaction_id}", response_model = schemas.TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id, models.Transaction.user_id == current_user.id).first()

    if not transaction:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Transaction not found")
    return transaction

@router.put("/transactions/{transaction_id}", response_model = schemas.TransactionResponse)
def update_transaction(transaction_id: int, updated_data: schemas.TransactionUpdate, db: Session = Depends(get_db),currrent_user: models.User = Depends(get_current_user)):
    transaction = db.query(models.Treansaction).filter(models.Transaction.id == transaction_id, models.Transaction.user_id == current_user.id).first()
    if not transaction:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Transaction not found")

    
    update_fields = updated_data.model_dump(exclude_unset=True)

    for field, value in update_fields.items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)
    return transaction

@router.delete("/transactions/{transaction_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id, models.Transaction.user_id == current_user.id).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    db.delete(transaction)
    db.commit()

    return None






