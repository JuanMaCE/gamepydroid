from users.user import User, create_user

class UserCreator:
    def __init__(self, repository):
        self.repository = repository

    def run(self, name: str, password: str, level: str):
        new_user = create_user(name, password, level)
        return self.repository.save(new_user)