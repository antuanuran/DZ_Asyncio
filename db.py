from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, JSON


DSN = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:5439/asincio_bd'
engine = create_async_engine(DSN)
Base = declarative_base()
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class People(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    json = Column(JSON, nullable=False)









