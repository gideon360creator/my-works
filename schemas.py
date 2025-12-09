from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class UserRole(str, Enum):
    student = "student"
    lecturer = "lecturer"

class UserBase(BaseModel):
    username: str
    role: UserRole

class UserCreate(UserBase):
    password: str
    # For students, registration must include their matriculation/student number (11 digits)
    student_number: Optional[str] = None

class User(UserBase):
    id: int
    student_number: Optional[str] = None
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class SubjectBase(BaseModel):
    name: str
    code: str

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    id: int
    class Config:
        from_attributes = True

class AssessmentBase(BaseModel):
    name: str
    max_score: float
    weight: float
    subject_id: int

class AssessmentCreate(AssessmentBase):
    pass

class Assessment(AssessmentBase):
    id: int
    class Config:
        from_attributes = True

class GradeBase(BaseModel):
    score: float
    # use matriculation/student number (11-digit string) in APIs instead of numeric DB id
    student_number: str
    assessment_id: int

class GradeCreate(GradeBase):
    pass

class Grade(GradeBase):
    id: int
    # For responses we expose the student's matriculation number (student_number)
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str


class GpaResponse(BaseModel):
    gpa: float
    percentage: float
    recorded_weight: float
    graded_assessments: int
    class Config:
        from_attributes = True
