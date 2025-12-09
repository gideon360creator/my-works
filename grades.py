from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

import models
import schemas
import auth
from database import get_db

router = APIRouter(
    prefix="/grades",
    tags=["grades"]
)

def require_lecturer(current_user: models.User = Depends(auth.get_current_user)):
    """Dependency to ensure the current user is a lecturer."""
    if current_user.role != schemas.UserRole.lecturer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Only lecturers can perform this action."
        )
    return current_user

@router.post("/", response_model=schemas.Grade, status_code=status.HTTP_201_CREATED)
def create_grade(grade: schemas.GradeCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_lecturer)):
    """
    Allows a lecturer to add a new grade for a student.
    """
    # Find the student by their student number
    student = db.query(models.User).filter(models.User.student_number == grade.student_number).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with number {grade.student_number} not found")

    # Check if the assessment exists
    assessment = db.query(models.Assessment).filter(models.Assessment.id == grade.assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail=f"Assessment with id {grade.assessment_id} not found")

    db_grade = models.Grade(
        student_id=student.id,
        assessment_id=grade.assessment_id,
        score=grade.score
    )
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.get("/", response_model=List[schemas.Grade])
def get_all_grades(db: Session = Depends(get_db), current_user: models.User = Depends(require_lecturer)):
    """
    Allows a lecturer to retrieve all grades from the system.
    """
    grades = db.query(models.Grade).options(joinedload(models.Grade.student)).all()
    return grades

@router.delete("/{grade_id}", response_model=schemas.Grade)
def delete_grade(grade_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(require_lecturer)):
    """
    Allows a lecturer to delete a specific grade by its ID.
    This is the backend functionality for the 'remove grade' button.
    """
    grade_to_delete = db.query(models.Grade).filter(models.Grade.id == grade_id).first()

    if not grade_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grade with id {grade_id} not found."
        )

    db.delete(grade_to_delete)
    db.commit()

    # The grade object is expired after commit, so we can't return it directly.
    # We can construct a response from the data we had before deleting.
    return grade_to_delete