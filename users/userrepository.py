from abc import ABC, abstractmethod
from users.user import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user:User):
        pass

    @abstractmethod
    def search(self, id: str) -> User:
        pass

