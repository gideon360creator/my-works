from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class UserRole(str, enum.Enum):
    student = "student"
    lecturer = "lecturer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String) # "student" or "lecturer"
    # Student number follows strict format like 22010301001 (11 digits) and is optional for non-students
    student_number = Column(String, unique=True, index=True, nullable=True)

    grades = relationship("Grade", back_populates="student")
    # For simplicity, we won't strictly link subjects to lecturers in the DB schema yet, 
    # but in a real app, we would.

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True, index=True)

    assessments = relationship("Assessment", back_populates="subject")

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    name = Column(String) # e.g., "Midterm", "Final", "Assignment 1"
    max_score = Column(Float)
    weight = Column(Float) # Percentage weight, e.g., 30.0 for 30%

    subject = relationship("Subject", back_populates="assessments")
    grades = relationship("Grade", back_populates="assessment")

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    assessment_id = Column(Integer, ForeignKey("assessments.id"))
    score = Column(Float)

    student = relationship("User", back_populates="grades")
    assessment = relationship("Assessment", back_populates="grades")

    @property
    def student_number(self):
        """
        Expose the student's matriculation number for API responses.
        Pydantic response models with Config.from_attributes=True can read this property.
        """
        try:
            return self.student.student_number if self.student else None
        except Exception:
            return None
