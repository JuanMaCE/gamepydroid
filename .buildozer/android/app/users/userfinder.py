from users.userrepository import UserRepository


class UserFinder:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def run(self, id: str):
        return self.repository.search(id)

    def update(self, id: str, level):
        return self.repository.update(id, level)

    def search_by_id(self, id: str):
        return self.repository.search_by_id(id)

    def search_top(self):
        return self.repository.search_top()