from abc import abstractmethod, ABC
from typing import TypeVar, Generic, Optional

T = TypeVar('T')
ID = TypeVar('ID')

class BaseServiceApi(ABC, Generic[T,ID]):

    @abstractmethod
    def save(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, id: ID) -> bool:
        pass

    @abstractmethod
    def get_all(self) -> list[T]:
        pass

    @abstractmethod
    def get_one_by_id(self, id: ID) -> Optional[T]:
        pass
