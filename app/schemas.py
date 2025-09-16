from pydantic import BaseModel

class AccountCreate(BaseModel):
    name: str

class AccountOut(BaseModel):
    id: int
    name: str
    balance: float
    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    account_id: int
    amount: float
    type: str
