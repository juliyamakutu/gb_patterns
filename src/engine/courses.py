from copy import deepcopy
from typing import Optional


class PrototypeMixin:
    def clone(self):
        return deepcopy(self)


class Course(PrototypeMixin):
    def __init__(self, name: str, category: "Category"):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class OfflineCourse(Course):
    pass


class OnlineCourse(Course):
    pass


class CourseFactory:
    types = {"offline": OfflineCourse, "online": OnlineCourse}

    @classmethod
    def create(cls, course_type: str, name: str, category: "Category"):
        return cls.types[course_type](name, category)


class Category:
    auto_id = 0

    def __init__(self, name: str, category: Optional["Category"] = None):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result
