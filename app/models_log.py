from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    headers = Column(Text)  # Store as JSON string
    path = Column(String)
    method = Column(String)
    status_code = Column(Integer)
    response_body = Column(Text)
    client_name = Column(String, nullable=True)
