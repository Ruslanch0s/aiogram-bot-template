from utils.db_api.db_gino import TimedBaseModel
from sqlalchemy import Column, BigInteger, String, sql


class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, unique=True)
    name = Column(String(100))
    email = Column(String(100))

    referral = Column(BigInteger)

    query: sql.Select  # выбор данных из таблицы
