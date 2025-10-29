from users.userrepository import UserRepository


class UserFinder:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def run(self, id: str):
        return self.repository.search(id)
