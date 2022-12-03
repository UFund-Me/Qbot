from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Float, create_engine

from web.database import Base
from web.settings import APISettings


class WatchStocks(Base):
    __tablename__ = 'watch_stocks'

    code = Column(String(10), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    watch_price = Column(Float, nullable=False)
    watch_time = Column(DateTime, nullable=False, default=datetime.now)
    close = Column(Float, nullable=False)


class Strategies(Base):
    __tablename__ = 'strategies'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True)
    code = Column(String(1024), nullable=False)
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(DateTime, nullable=False, default=datetime.now)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    roles = Column(String(1024), nullable=False)
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(DateTime, nullable=False, default=datetime.now)

if __name__ == '__main__':
    settings = APISettings()
    SQLALCHEMY_DATABASE_URL = f'sqlite:///../pytrader.db'
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
    )
    Base.metadata.create_all(engine)
