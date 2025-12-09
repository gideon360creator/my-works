from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import auth
from database import get_db

router = APIRouter(
    prefix="/subjects",
    tags=["subjects"]
)

def require_lecturer(current_user: models.User = Depends(auth.get_current_user)):
    """Dependency to ensure the current user is a lecturer."""
    if current_user.role != schemas.UserRole.lecturer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Only lecturers can perform this action."
        )
    return current_user

@router.post("/", response_model=schemas.Subject, status_code=status.HTTP_201_CREATED)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_lecturer)):
    db_subject = db.query(models.Subject).filter(models.Subject.code == subject.code).first()
    if db_subject:
        raise HTTPException(status_code=400, detail="Subject with this code already exists")
    
    db_subject = models.Subject(name=subject.name, code=subject.code)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.get("/", response_model=List[schemas.Subject])
def get_all_subjects(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    subjects = db.query(models.Subject).all()
    return subjects

@router.put("/{subject_id}", response_model=schemas.Subject)
def update_subject(subject_id: int, subject: schemas.SubjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_lecturer)):
    db_subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    # Check if the new code already exists
    if db.query(models.Subject).filter(models.Subject.code == subject.code, models.Subject.id != subject_id).first():
        raise HTTPException(status_code=400, detail="Subject with this code already exists")

    db_subject.name = subject.name
    db_subject.code = subject.code
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(require_lecturer)):
    db_subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    # Also delete associated assessments and grades
    db.query(models.Assessment).filter(models.Assessment.subject_id == subject_id).delete()
    
    db.delete(db_subject)
    db.commit()
    return
