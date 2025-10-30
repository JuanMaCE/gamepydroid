from abc import ABC, abstractmethod
from users.user import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user:User):
        pass

    @abstractmethod
    def search(self, id: str) -> User:
        pass

    @abstractmethod
    def update(self, id: str, level: str):
        pass

    @abstractmethod
    def search_by_id(self, id: str):
        pass

    @abstractmethod
    def search_top(self):
        pass