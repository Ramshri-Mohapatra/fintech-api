from pydantic import BaseModel, EmailStr
from datetime import datetime   
from typing import Optional
from app.models import TransactionType

"Schemas for user and transaction data validation and serialization using Pydantic models."

class UserCreate(BaseModel):    
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime    
    class Config:
        from_attribute = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 


class TransactionCreate(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    type: TransactionType

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    type: Optional[TransactionType] = None   
           
class TransactionResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: Optional[str] = None
    type: TransactionType
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True         