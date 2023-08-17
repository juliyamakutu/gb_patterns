import sqlite3
from threading import local

from .exceptions import (CommitException, DeleteException,
                         RecordNotFoundException, UpdateException)

connection = sqlite3.connect("patterns.sqlite")


class UnitOfWork:
    current = local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, mapper_registry):
        self.mapper_registry = mapper_registry

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

        self.new_objects.clear()
        self.dirty_objects.clear()
        self.removed_objects.clear()

    def insert_new(self):
        for obj in self.new_objects:
            self.mapper_registry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            self.mapper_registry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            self.mapper_registry.get_mapper(obj).delete(obj)

    @classmethod
    def new_current(cls):
        cls.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


class StudentMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table_name = "student"

    def all(self):
        statement = f"SELECT * from {self.table_name}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(
                f"Record with id={id} not found in table {self.table_name}"
            )

    def insert(self, obj):
        statement = f"INSERT INTO {self.table_name} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise CommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.table_name} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise UpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DeleteException(e.args)


class MapperRegistry:
    mappers = {
        "student": StudentMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class User(DomainObject):
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
