from users.username import UserName
from users.usermaxlevel import UserMaxLevel
from users.userpassword import UserPassword
from users.userdto import UserDTO



class User:
    def __init__(self, name: UserName, password: UserPassword, level: UserMaxLevel):
        self._name = name
        self._password = password
        self._level = level

    def to_dto(self):
        return UserDTO(self._name.name, self._password.password, self._level.level)

def create_user(name: str, password: str, level: str)-> User:
    create_name = UserName(name)
    create_password = UserPassword(password)
    create_level = UserMaxLevel(level)
    return  User(create_name, create_password, create_level)



