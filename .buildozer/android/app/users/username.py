def isValid(data:str):
    if len(data) > 3:
        return data


class UserName:
    def __init__(self, data:str):
        self.name = isValid(data)
