from fastapi import FastAPI, Depends, HTTPException, status, Request, Query, File, UploadFile, status

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List,Annotated
from starlette.middleware.cors import CORSMiddleware
import crud, schemas, models, database, price
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import tempfile
import os

app = FastAPI()

origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# Dependency to get the database session.
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.on_event("startup")
def on_startup():
    database.Base.metadata.create_all(bind=database.engine)



#exception_handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred"},
    )

#Asset

@app.post("/assets/", response_model=schemas.AssetIndex)
def create_asset(asset_index: schemas.AssetIndexCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_asset(db=db, asset_index_create=asset_index)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/assets/", response_model=List[schemas.AssetIndex])
def read_assets(db: Session = Depends(get_db)):
    try:
        return crud.get_all_assets(db=db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@app.delete("/assets/{id}", response_model=schemas.AssetIndex)
def delete_asset(id: str, db: Session = Depends(get_db)):
    try:
        db_asset = crud.get_asset(db, id=id)
        if db_asset is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
        return crud.delete_asset(db, id=id)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@app.patch("/assets/{id}/")
def update_asset_quantity(
    id: str,
    quantity_update: schemas.AssetQuantityUpdate,
    db: Session = Depends(get_db)
):
    try:
        
        return crud.update_asset_quantity(db, id, quantity_update.quantity)
    except Exception as e:
  
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/total_quantity/{asset_id}")
def read_total_quantity(asset_id: str, db: Session = Depends(get_db)):
    try:
        total_quantity = crud.get_total_quantity_by_asset_id(db, asset_id)
        return {"asset_id": asset_id, "total_quantity": total_quantity}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.get("/all_total_quantity/")
def read_all_total_quantity( db: Session = Depends(get_db)):
    try:
        total_quantity = crud.get_total_quantity(db)
        return total_quantity
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    



#Transaction


@app.post("/transaction/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_transaction(db=db, transaction=transaction)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete("/transaction/{transaction_id}", response_model=schemas.Transaction)
def delete_transaction(transaction_id: str, db: Session = Depends(get_db)):
    try:
        db_transaction = crud.get_transaction(db, transaction_id=transaction_id)
        if db_transaction is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        return crud.delete_transaction(db, transaction_id=transaction_id)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/transaction/", response_model=List[schemas.Transaction])
def read_transactions(db: Session = Depends(get_db)):
    try:
        return crud.get_all_transaction(db=db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    


#Stock and Cryptocurrencies 
@app.get("/get_current_price/")
async def get_current_price(ticker: str):
    try:  
        return await price.get_current_price(ticker)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/get_current_prices/")
async def get_current_prices(db: Session = Depends(get_db)):
    try:  
        return await price.get_current_prices(db=db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@app.get("/get_total_value/")
async def get_total_value(db: Session = Depends(get_db)):
    try:  
        return await price.get_total_value(db=db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/predict_AAPL/")
def predict_AAPL_updown(db: Session = Depends(get_db)):
    try:
       return price.predict_AAPL_updown(db=db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.get("/get_total_value_by_asset/")
async def get_total_value_by_asset(db: Session = Depends(get_db)):
    try:  
        return await price.get_total_value_by_asset(db=db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@app.get("/ticker_data/{ticker}")
async def get_ticker_data(ticker: str):
    try:
       return await price.get_ticker_data(ticker)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.get("/asset_distribution_by_type/")
async def get_asset_distribution_by_type(db: Session = Depends(get_db)):
    try:
        return await price.get_assettype_distribution(db=db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@app.get("/asset_distribution_by_location/")
async def get_asset_distribution_by_location(db: Session = Depends(get_db)):
    try:
        return await price.get_assetlocation_distribution(db=db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.get("/historical_values/", response_model=list[schemas.PortfolioValueSchema])
async def get_historical_values(db: Session = Depends(get_db)):
    return db.query(models.PortfolioValue).all()



scheduler = AsyncIOScheduler()


scheduler.add_job(func=price.save_total_value,
    trigger=CronTrigger(hour='0,12'),
    args=(next(get_db()),),
    misfire_grace_time=120)

@app.on_event("startup")
async def start_scheduler():
    scheduler.start()


'''

@app.post("/excel_to_db/")
async def excel_to_db(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file format.")

    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name

        result = await crud.excel_to_db(db=db, file=temp_file_path)
        
        return result
    except Exception as e:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            '''