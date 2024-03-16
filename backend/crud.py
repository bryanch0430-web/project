from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas

class IndexNotFoundError(Exception):
    pass


# AssetIndex
def get_all_assets(db: Session):
    return db.query(models.AssetIndex).all()

def create_asset(asset_index_create: schemas.AssetIndexCreate, db: Session):
    db_asset_index = models.AssetIndex(**asset_index_create.dict())
    db.add(db_asset_index)
    db.commit()
    db.refresh(db_asset_index)
    return db_asset_index

def get_all_unique_asset_id(db: Session):
    return db.query(models.AssetIndex.asset_id).distinct().all()

def get_asset(db: Session, id: str):
    db_asset = db.query(models.AssetIndex).filter(models.AssetIndex.id == id).first()
    if db_asset:
        return db_asset
    else:
        raise IndexNotFoundError(f"Asset with id {id} does not exist.")



def delete_asset(db: Session, id: str):
    db_asset = get_asset(db, id)
    db.delete(db_asset)
    db.commit()
    return db_asset

def update_asset_quantity(db: Session, id: str, quantity: float):
    db_asset = get_asset(db, id)
    db_asset.quantity = quantity
    db.commit()
    db.refresh(db_asset)
    return db_asset

#quantity
def get_total_quantity_by_asset_id(db: Session, asset_id: str):
  
    total_quantity = (
        db.query(models.AssetIndex)
        .filter(models.AssetIndex.asset_id == asset_id)
        .with_entities(func.sum(models.AssetIndex.quantity))
        .scalar()
    )

    return total_quantity if total_quantity else 0.0

def get_total_quantity(db: Session):
    asset_id_list = get_all_unique_asset_id(db)
    total_quantity = {}
    for row in asset_id_list:
        total_quantity[row.asset_id] = get_total_quantity_by_asset_id(db, row.asset_id)
    return total_quantity




# Transaction
def get_transaction(db: Session, transaction_id: str):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.transaction_id == transaction_id).first()
    if db_transaction:
        return db_transaction
    else:
        raise IndexNotFoundError(f"Transaction with id {transaction_id} does not exist.")

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: str):
    db_transaction = get_transaction(db, transaction_id)
    db.delete(db_transaction)
    db.commit()
    return db_transaction

def get_all_transaction(db: Session):
    return db.query(models.Transaction).all()