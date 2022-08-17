from sqlalchemy import Column, Integer, String
from sqlalchemy import orm

from .database import Base


class Registration(Base):
    __tablename__ = 'registration'

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=True)
    code_ver = Column(Integer, nullable=True)
    data = orm.relation("Data", back_populates='user')
    data_page = orm.relation('PageData', back_populates='page')

    def __repr__(self):
        info: str = f'Пользователь [ID: {self.id}, Почта: {self.address}' \
                    f', Код: {self.code_ver}]'

        return info