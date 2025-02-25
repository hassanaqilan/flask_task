import time


class Student:
    def __init__(self, id: int, name: str, age: int, grade: int):
        self.id = id
        self.name = name
        self.age = age
        self.grade = grade

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
