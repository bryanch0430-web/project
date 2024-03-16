import yfinance as yf
from fastapi import  HTTPException
from fastapi.responses import JSONResponse
from typing import List
import asyncio

async def get_current_price(ticker: str):
    data = yf.Ticker(ticker).history(period='1y')
    return JSONResponse({
        'current_price': data.iloc[-1].Close
    })

# aovid blocking the event loop
async def fetch_price(ticker: str):
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: yf.Ticker(ticker).history(period='1d'))
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} data not found")
    return {
        'ticker': ticker,
        'current_price': data.iloc[-1].Close
    }

async def get_current_prices(tickers: List[str]):
    tasks = [fetch_price(ticker) for ticker in tickers]
    prices = await asyncio.gather(*tasks, return_exceptions=True)  
    results = []
    for price in prices:
        if isinstance(price, Exception):
            results.append({'error': str(price)})
        else:
            results.append(price)
    return JSONResponse(results)

