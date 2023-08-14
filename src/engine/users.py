class User:
    def __init__(self, name: str):
        self.name = name


class Teacher(User):
    pass


class Student(User):
    pass


class UserFactory:
    types = {
        "student": Student,
        "teacher": Teacher,
    }

    @classmethod
    def create(cls, user_type: str, name: str):
        return cls.types[user_type](name)
