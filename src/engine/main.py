from typing import Optional

from .courses import Category, Course, CourseFactory
from .users import User, UserFactory


class Engine:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(user_type: str, name: str) -> User:
        return UserFactory.create(user_type, name)

    @staticmethod
    def create_category(name: str, category: Optional[Category] = None) -> Category:
        return Category(name, category)

    def get_category(self, category_id: int) -> Optional[Category]:
        for item in self.categories:
            if item.id == category_id:
                return item
        return None

    @staticmethod
    def create_course(course_type: str, name: str, category: Category) -> Course:
        return CourseFactory.create(course_type, name, category)

    def get_course(self, name: str) -> Optional[Course]:
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name: str) -> Optional[User]:
        for item in self.students:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val: str) -> str:
        return val.replace("%", "=").replace("+", " ").encode("UTF-8").decode("UTF-8")
