from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base 
from datetime import datetime

class AssetIndex(Base):
    __tablename__ = "asset_index"
    id = Column(String, primary_key=True)
    asset_id = Column(String, nullable=False)
    asset_type = Column(String, nullable=False)
    description = Column(String)
    location = Column(String, nullable=False)
    quantity = Column(Float)
    cost_price = Column(Float)
    transactions = relationship("Transaction", back_populates="asset_index")


class Transaction(Base):
    __tablename__ = 'transactions'
    
    transaction_id = Column(String, primary_key=True)
    asset_index_id = Column(String, ForeignKey('asset_index.id'))
    quantity = Column(Float)
    buying_date = Column(DateTime)
    buying_price = Column(Float)
    
    asset_index = relationship("AssetIndex" ,foreign_keys = asset_index_id ,back_populates="transactions")

class Prediction(Base):
    __tablename__ = 'prediction_result'
    date = Column(DateTime, primary_key=True)
    trend = Column(String)
    
    
class PortfolioValue(Base):
    __tablename__ = "portfolio_values"
    timestamp = Column(DateTime, primary_key=True, index=True, default=datetime.utcnow)
    total_value = Column(Float)
    
    
#Asset
#primary_key |unique     |nullable 
# id         |asset_id   |asset_type
    
#Asset Quantity
#primary_key | !nullable 
#id          | !qunatiy  
    
#transaction
#primary_key |foreign_key |foreign_key|!nullable|!nullable   | !nullable
# id         |id   (Asset)|type(Asset)| qunatiy |buying_date | buying_price


# type: crypto stock save house 