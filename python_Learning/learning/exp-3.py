class Student(object):
    pass

def set_age(self, age):
    self.age = age
s = Student()
from types import MethodType
s.set_age = MethodType(set_age, s) 
s.set_age(25)
print(s.age)
