import yfinance as yf
from fastapi import  HTTPException
from fastapi.responses import JSONResponse
from typing import List
import asyncio
import models, schemas
from sqlalchemy.orm import Session

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
    return JSONResponse(results)
