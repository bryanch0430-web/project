import numpy as np
import yfinance as yf
from fastapi import  HTTPException
from fastapi.responses import JSONResponse
from typing import List
import asyncio
import models, crud ,schemas
from sqlalchemy.orm import Session
import tensorflow as tf
from datetime import datetime, timedelta

async def get_current_price(ticker: str):
    data = yf.Ticker(ticker).history(period='1y')
    return JSONResponse({
        'current_price': data.iloc[-1].Close
    })

# aovid blocking the event loop
async def fetch_price(ticker_tuple: tuple):
    ticker = ticker_tuple[0]  
    loop = asyncio.get_event_loop()
    try:
        data = await loop.run_in_executor(None, lambda: yf.Ticker(ticker).history(period='1d'))
        if data.empty:
            raise HTTPException(status_code=404, detail=f"Ticker {ticker} data not found")
        return {
            'ticker': ticker,
            'current_price': data.iloc[-1].Close
        }
    except Exception as e:
        return {'error': str(e)}

async def get_current_prices(db: Session):
    tickers = db.query(models.AssetIndex.asset_id).distinct().all()
    tasks = [fetch_price(ticker) for ticker in tickers]
    prices = await asyncio.gather(*tasks, return_exceptions=True)
    results = []
    for price in prices:
        if isinstance(price, dict) and "error" in price:
            results.append(price)
        else:
            results.append(price)
    return results



async def get_total_value(db: Session):
    prices = await get_current_prices(db)
    quantities = crud.get_total_quantity(db)
    total_value = 0.0

    for price in prices:
        if 'error' not in price:
            asset_id = price['ticker']
            quantity = quantities.get(asset_id, 0.0)
            total_value += quantity * price['current_price']

    return total_value

            
def reshape_input(data, time_steps):
    X = []

    for i in range(len(data) - time_steps):
        X.append(data[i:i + time_steps])

    return np.array(X)


def predict_AAPL_updown(db: Session):
    buffer_days = 150 
    time_steps = 100  
    start_date = (datetime.today() - timedelta(days=time_steps + buffer_days)).strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')
    ticker = yf.Ticker('AAPL')
    df = ticker.history(start=start_date, end=end_date)

    if df.empty:
        return {"detail": "No data was retrieved from yfinance."}
    
    df.drop(columns=["Dividends", "Stock Splits"], inplace=True)

    if len(df) < time_steps:
        return {"detail": "Not enough data to create a valid input window."}

    data = df.to_numpy()
    APPL_model = tf.keras.models.load_model('AAPLpredictionUNetTimeSeries_55%.keras')
    data_reshaped = reshape_input(data, time_steps)

    if data_reshaped.shape[0] == 0:
        return {"detail": "No input windows could be created from the available data."}

    last_window = data_reshaped[-1].reshape(1, time_steps,5)
    prediction = APPL_model.predict(last_window)

    if prediction.tolist() == [[1,0]]:
        a = 'up'
    else:
        a = 'down'  
    
    today = datetime.today()
    existing_prediction = db.query(models.Prediction).filter(models.Prediction.date == today).first()
    if not existing_prediction:
        prediction_data = schemas.PredictionCreate(date=today, trend=a)
        crud.create_prediction(db,prediction_data)
    return a


