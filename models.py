from sqlalchemy import Column, String
from db_setup import Base, engine

class AlertChannel(Base):
    __tablename__ = 'alert_channels'
    channel_id = Column(String, primary_key=True)

    def __init__(self, channel_id):
        self.channel_id = channel_id

Base.metadata.create_all(bind=engine)