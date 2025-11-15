def isValid(data:str):
    if len(data) >= 6:
        return data


class UserPassword:
    def __init__(self, data:str):
        self.password = isValid(data)
