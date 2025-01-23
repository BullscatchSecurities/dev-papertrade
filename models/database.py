from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
    Enum
)

from datetime import datetime
from utils.database import Base, engine
from pydantic import BaseModel
import logging


class TransactionTypeEnum(Enum):
    BUY = "BUY"
    SELL = "SELL"
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    tradingSymbol = Column(String, nullable=False)
    exchange = Column(String, nullable=False)
    transactionType = Column(Enum(TransactionTypeEnum), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    trigger_price = Column(Integer, nullable=False)
    disclosed_price = Column(Integer, nullable=False)
    validity = Column(String, nullable=False)
    status = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tables created successfully.")
