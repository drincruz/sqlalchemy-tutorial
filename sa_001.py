"""
SQLAlchemy setup and quick test

"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(Department, backref=backref('employees', uselist=True))


from sqlalchemy import create_engine

engine = create_engine('sqlite:///')

from sqlalchemy.orm import sessionmaker

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)


"""
Test our set up by inserting several example records

"""
john = Employee(name='john')
it_department = Department(name='IT')
john.department = it_department

s = session()
s.add(john)
s.add(it_department)
s.commit()
it = s.query(Department).filter(Department.name == 'IT').one()
print(it.employees[0].name)

"""
Continuing with tutorial
learning some SQLAlchemy SELECTs

"""
from sqlalchemy import select

find_it = select([Department.id]).where(Department.name == 'IT')
rs = s.execute(find_it)
print(rs)

print(rs.fetchone())

find_john = select([Employee.id]).where(Employee.department_id == 1)
rs = s.execute(find_john)
print(rs.fetchone())
