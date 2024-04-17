from uuid import UUID, uuid4

from decorators import Entity
from abstracts import DAO


@Entity(name='sports', pk='id')
class SportsDAO(DAO):
    id: UUID
    name: str
    teacher_name: str
    total_students: int
    location: str

    def __init__(self,
                 name: str = None,
                 teacher_name: str = None,
                 total_students: int = None,
                 location: str = None,
                 ):
        self.id = uuid4()
        self.name = name
        self.teacher_name = teacher_name
        self.total_students = total_students
        self.location = location
        super().__init__()
