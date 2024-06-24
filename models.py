from sqlalchemy import Column, DateTime, Float, String
from db_setup import Base, engine

class AlertChannel(Base):
    __tablename__ = 'alert_channels'
    channel_id = Column(String, primary_key=True)

    def __init__(self, channel_id):
        self.channel_id = channel_id

class RelativeStrengthIndex(Base):
    __tablename__ = 'rsi'
    symbol = Column(String, primary_key=True)
    rsi = Column(Float)
    latest_bar_close_at = Column(DateTime)


    def __init__(self, symbol, rsi, latest_bar_close_at):
        self.symbol = symbol
        self.rsi = rsi
        self.latest_bar_close_at = latest_bar_close_at

Base.metadata.create_all(bind=engine)