from fastapi import FastAPI
from pydantic import BaseModel

from sport_dao import SportsDAO
from student_dao import StudentDAO
from repository import Repository

app = FastAPI()


class StudentDto(BaseModel):
    name: str
    lastname: str
    current_school_year: int
    birthday_year: int
    birthday_month: int
    birthday_day: int
    emergency_contact: str

    def to_student_dao(self):
        return StudentDAO(
            name=self.name,
            lastname=self.lastname,
            current_school_year=self.current_school_year,
            birthday_day=self.birthday_day,
            birthday_month=self.birthday_month,
            birthday_year=self.birthday_year,
            emergency_contact=self.emergency_contact
        )


class SportDto(BaseModel):
    name: str
    teacher_name: str
    total_students: int
    location: str

    def to_sports_dao(self):
        return SportsDAO(
            name=self.name,
            teacher_name=self.teacher_name,
            total_students=self.total_students,
            location=self.location
        )


@app.get("/students")
async def get_students():
    result = Repository.list_all(StudentDAO)
    return result


@app.post("/students")
async def create_student(student_dto: StudentDto):
    student = student_dto.to_student_dao()
    Repository.persist(student)
    return {
        "id": student.id
    }


@app.get("/sports")
async def get_sports():
    result = Repository.list_all(SportsDAO)
    return result


@app.post("/sports")
async def create_sport(sport_dto: SportDto):
    sport = sport_dto.to_sports_dao()
    Repository.persist(sport)
    return {
        "id": sport.id
    }


@app.get("/health")
async def health():
    return True
