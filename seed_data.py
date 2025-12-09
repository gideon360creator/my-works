"""
Script to seed the database with sample data for testing the chatbot
"""
import sys
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import auth

def seed_database():
    db = SessionLocal()
    
    try:
        # Check if we already have data
        existing_subjects = db.query(models.Subject).count()
        if existing_subjects > 0:
            print("Database already has data. Skipping seed.")
            return
        
        print("Seeding database with sample data...")
        
        # Create subjects
        math = models.Subject(name="Mathematics", code="MATH101")
        physics = models.Subject(name="Physics", code="PHYS101")
        cs = models.Subject(name="Computer Science", code="CS101")
        
        db.add_all([math, physics, cs])
        db.commit()
        db.refresh(math)
        db.refresh(physics)
        db.refresh(cs)
        print("✓ Created subjects")
        
        # Create assessments for Mathematics
        math_midterm = models.Assessment(
            subject_id=math.id,
            name="Midterm Exam",
            max_score=100,
            weight=30.0
        )
        math_final = models.Assessment(
            subject_id=math.id,
            name="Final Exam",
            max_score=100,
            weight=40.0
        )
        math_assignment = models.Assessment(
            subject_id=math.id,
            name="Assignments",
            max_score=100,
            weight=30.0
        )
        
        # Create assessments for Physics
        physics_midterm = models.Assessment(
            subject_id=physics.id,
            name="Midterm Exam",
            max_score=100,
            weight=35.0
        )
        physics_final = models.Assessment(
            subject_id=physics.id,
            name="Final Exam",
            max_score=100,
            weight=40.0
        )
        physics_lab = models.Assessment(
            subject_id=physics.id,
            name="Lab Work",
            max_score=100,
            weight=25.0
        )
        
        # Create assessments for Computer Science
        cs_midterm = models.Assessment(
            subject_id=cs.id,
            name="Midterm Exam",
            max_score=100,
            weight=30.0
        )
        cs_project = models.Assessment(
            subject_id=cs.id,
            name="Final Project",
            max_score=100,
            weight=40.0
        )
        cs_quizzes = models.Assessment(
            subject_id=cs.id,
            name="Quizzes",
            max_score=100,
            weight=30.0
        )
        
        db.add_all([
            math_midterm, math_final, math_assignment,
            physics_midterm, physics_final, physics_lab,
            cs_midterm, cs_project, cs_quizzes
        ])
        db.commit()
        print("✓ Created assessments")
        
        # Get the first student user (or create a demo one)
        student = db.query(models.User).filter(models.User.role == "student").first()
        
        if not student:
            print("No student user found. Creating demo student...")
            hashed_password = auth.get_password_hash("demo123")
            demo_student_number = "22010301001"
            student = models.User(
                username=demo_student_number,
                hashed_password=hashed_password,
                role="student",
                student_number=demo_student_number
            )
            db.add(student)
            db.commit()
            db.refresh(student)
            print(f"✓ Created demo student (matriculation: {demo_student_number}, password: demo123)")
        
        # Refresh assessments to get their IDs
        db.refresh(math_midterm)
        db.refresh(math_final)
        db.refresh(math_assignment)
        db.refresh(physics_midterm)
        db.refresh(physics_final)
        db.refresh(physics_lab)
        db.refresh(cs_midterm)
        db.refresh(cs_project)
        db.refresh(cs_quizzes)
        
        # Create sample grades for the student
        grades = [
            # Mathematics grades (Good performance)
            models.Grade(student_id=student.id, assessment_id=math_midterm.id, score=85),
            models.Grade(student_id=student.id, assessment_id=math_final.id, score=88),
            models.Grade(student_id=student.id, assessment_id=math_assignment.id, score=92),
            
            # Physics grades (Average performance)
            models.Grade(student_id=student.id, assessment_id=physics_midterm.id, score=75),
            models.Grade(student_id=student.id, assessment_id=physics_final.id, score=78),
            models.Grade(student_id=student.id, assessment_id=physics_lab.id, score=82),
            
            # Computer Science grades (Excellent performance)
            models.Grade(student_id=student.id, assessment_id=cs_midterm.id, score=95),
            models.Grade(student_id=student.id, assessment_id=cs_project.id, score=98),
            models.Grade(student_id=student.id, assessment_id=cs_quizzes.id, score=93),
        ]
        
        db.add_all(grades)
        db.commit()
        print(f"✓ Created {len(grades)} sample grades for student: {student.username}")
        
        print("\n✅ Database seeded successfully!")
        print(f"\nYou can now login with:")
        print(f"  Matriculation / Username: {student.username}")
        print(f"  Password: demo123")
        print("\nTry asking the chatbot:")
        print("  - 'What is my grade in Mathematics?'")
        print("  - 'How am I performing?'")
        print("  - 'What do I need to get an A in Physics?'")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

def clear_database():
    """Deletes all the sample data from the database."""
    db = SessionLocal()
    try:
        print("Clearing database of sample data...")

        # The order of deletion is important to avoid foreign key violations.
        # We delete in the reverse order of creation.

        num_grades = db.query(models.Grade).delete()
        num_assessments = db.query(models.Assessment).delete()
        num_subjects = db.query(models.Subject).delete()

        # Be specific about deleting the demo student
        demo_student_number = "22010301001"
        student = db.query(models.User).filter(models.User.student_number == demo_student_number).first()
        if student:
            db.delete(student)
            print(f"✓ Deleted demo student: {demo_student_number}")

        db.commit()
        print(f"✓ Deleted {num_grades} grades, {num_assessments} assessments, and {num_subjects} subjects.")
        print("\n✅ Database cleared successfully!")

    except Exception as e:
        print(f"Error clearing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'clear':
        clear_database()
    else:
        seed_database()
