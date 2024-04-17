from uuid import UUID, uuid4

from decorators import Entity
from abstracts import DAO


@Entity(name='students', pk='id')
class StudentDAO(DAO):
    id: UUID
    name: str
    lastname: str
    current_school_year: int
    birthday_year: int
    birthday_month: int
    birthday_day: int
    emergency_contact: str

    def __init__(self,
                 name: str = None,
                 lastname: str = None,
                 current_school_year: int = None,
                 birthday_year: int = None,
                 birthday_month: int = None,
                 birthday_day: int = None,
                 emergency_contact: str = None
                 ):
        self.id = uuid4()
        self.name = name
        self.lastname = lastname
        self.current_school_year = current_school_year
        self.birthday_year = birthday_year
        self.birthday_month = birthday_month
        self.birthday_day = birthday_day
        self.emergency_contact = emergency_contact
        super().__init__()
