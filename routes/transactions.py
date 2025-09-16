from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database, kafka_producer

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/")
def create_transaction(txn: schemas.TransactionCreate, db: Session = Depends(database.get_db)):
    account = db.query(models.Account).filter(models.Account.id == txn.account_id).first()
    if not account:
        return {"error": "Account not found"}

    if txn.type == "debit" and account.balance < txn.amount:
        return {"error": "Insufficient funds"}

    if txn.type == "credit":
        account.balance += txn.amount
    elif txn.type == "debit":
        account.balance -= txn.amount

    transaction = models.Transaction(account_id=txn.account_id, amount=txn.amount, type=txn.type)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    # Push event to Kafka
    kafka_producer.send_event("transactions", {
        "account_id": txn.account_id,
        "amount": txn.amount,
        "type": txn.type
    })

    return {"message": "Transaction successful", "balance": account.balance}
