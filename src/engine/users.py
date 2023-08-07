class User:
    pass


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
    def create(cls, user_type: str):
        return cls.types[user_type]()
