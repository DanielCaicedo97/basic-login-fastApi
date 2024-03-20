from common.base_service_api import BaseServiceApi
from typing import TypeVar, Optional

from sqlmodel import select
from config.db_config import get_session

T = TypeVar('T')
ID = TypeVar('ID')

class BaseServiceImpl(BaseServiceApi[T, ID]):

    def __init__(self):
        pass

    def save(self, entity: T) -> T:

        with get_session() as db:
            db.add(entity)
            db.commit()
            return entity
  

    def delete(self, id: ID) -> bool:
        try:
            with get_session() as db:
                statement = select(self.model).where(self.model.id == id)
                result = db.exec(statement).first()
                db.delete(result)
                db.commit()
                return True
        except Exception as e:
            return False

    def get_all(self) -> list[T]:
        try:
            with get_session() as db:
                statement = select(self.model)
                result = db.exec(statement).all()
                return result
        except Exception as e:
            return []

    def get_one_by_id(self, id: ID) -> Optional[T]:
        try:
            with get_session() as db:
                statement = select(self.model).where(self.model.id == id)
                result = db.exec(statement).first()
                return result
        except Exception as e:
            return None
