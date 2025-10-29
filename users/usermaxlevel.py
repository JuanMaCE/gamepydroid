def isValid(data: str) -> int:
    try:
        new_level = int(data)
        return new_level
    except ValueError:
        return 0


class UserMaxLevel:
    def __init__(self, data: str):
        self.level = isValid(data)


