from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from typing import Dict, Any


# AssetIndex Models
class AssetIndexBase(BaseModel):
    id: str
    asset_id: str
    asset_type: str
    description:str
    location: str
    quantity: float
    cost_price: float


class AssetQuantityUpdate(BaseModel):
    quantity: float

class AssetIndexCreate(AssetIndexBase):
    pass

class AssetIndex(AssetIndexBase):

    class Config:
        orm_mode = True

# Transaction Models
class TransactionBase(BaseModel):
    transaction_id: str
    asset_index_id: str
    quantity: float
    buying_date: datetime
    buying_price: float

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    class Config:
        orm_mode = True


#Prediction result storing
class PredictionBase(BaseModel):
    date:datetime
    trend: str
    
class PredictionCreate(PredictionBase):
    pass

class Prediction(PredictionBase):
    class Config:
        orm_mode = True
        
class TickerData(BaseModel):
    data: dict

class AssetDistribution(BaseModel):
    asset_distribution: dict
    
class PortfolioValueSchema(BaseModel):
    timestamp: datetime
    total_value: float

    class Config:
        orm_mode = True