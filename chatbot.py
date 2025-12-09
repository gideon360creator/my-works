import re
from sqlalchemy.orm import Session
import logic
import models

def process_query(query: str, db: Session, user_id: int) -> str:
    query = query.lower()
    
    # Pattern: "What is my grade in [Subject]?"
    # Improved regex to handle "grade for", "grades in", "grades for"
    match_grade = re.search(r"grades? (?:in|for) (.+)", query)
    if match_grade:
        raw_subject = match_grade.group(1).strip("?").strip()

        # Try to extract a subject name and optional code e.g. "Mathematics (MATH101)" or "Mathematics MATH101"
        name_part = raw_subject
        code_part = None
        m = re.match(r"^(.+?)\s*\(([^)]+)\)$", raw_subject)
        if m:
            name_part = m.group(1).strip()
            code_part = m.group(2).strip()
        else:
            # also accept formats like "Mathematics MATH101"
            parts = raw_subject.split()
            if len(parts) > 1 and re.fullmatch(r"[A-Za-z0-9]+", parts[-1]):
                code_part = parts[-1].strip()
                name_part = " ".join(parts[:-1]).strip()

        # 1. Find the subject(s) first: search by name or code when available
        query_filter = models.Subject.name.ilike(f"%{name_part}%")
        if code_part:
            subjects = db.query(models.Subject).filter(
                (models.Subject.name.ilike(f"%{name_part}%")) | (models.Subject.code.ilike(f"%{code_part}%"))
            ).all()
        else:
            subjects = db.query(models.Subject).filter(query_filter).all()

        if not subjects:
            return f"I couldn't find any subject matching '{raw_subject}'."
            
        response_parts = []
        
        for subject in subjects:
            # 2. Find grades for this subject
            grades = db.query(models.Grade).join(models.Assessment).filter(
                models.Grade.student_id == user_id,
                models.Assessment.subject_id == subject.id
            ).all()
            
            if grades:
                part = f"**{subject.name}** ({subject.code}):\n"
                total_score = 0
                total_weight = 0
                
                for grade in grades:
                    part += f"- {grade.assessment.name}: {grade.score} ({logic.calculate_grade_letter(grade.score)})\n"
                    total_score += grade.score * (grade.assessment.weight / 100)
                    total_weight += grade.assessment.weight
                
                part += f"Current Weighted Score: {total_score:.1f} (out of {total_weight} weight so far)\n"
                response_parts.append(part)
            else:
                # 3. If no grades, check for assessments
                assessments = db.query(models.Assessment).filter(
                    models.Assessment.subject_id == subject.id
                ).all()
                
                if assessments:
                    assessment_names = ", ".join([f"{a.name} ({a.weight}%)" for a in assessments])
                    response_parts.append(f"**{subject.name}**: No grades recorded yet. Assessments: {assessment_names}.")
                else:
                    response_parts.append(f"**{subject.name}**: No grades or assessments found.")

        return "\n".join(response_parts)

    # Pattern: "How am I performing?"
    if "performing" in query or "performance" in query or "summary" in query:
        stats = logic.get_student_performance_summary(db, user_id)
        if isinstance(stats, str): return stats
        return (f"Performance Summary:\n"
                f"GPA: {stats['gpa']}\n"
                f"Best Subject: {stats['best_subject']}\n"
                f"Needs Improvement: {stats['worst_subject']}")

    # Pattern: "What do I need to score to get a [Grade]?"
    # This is tricky without context of which subject. 
    # We'll assume the user might say "What do I need for an A in Math?"
    match_prediction = re.search(r"need.*get a ([a-f]) in (.+)", query)
    if match_prediction:
        target_grade = match_prediction.group(1).upper()
        subject_name = match_prediction.group(2).strip("?").strip()
        
        # Get current standing
        grades = db.query(models.Grade).join(models.Assessment).join(models.Subject).filter(
            models.Grade.student_id == user_id,
            models.Subject.name.ilike(f"%{subject_name}%")
        ).all()
        
        if not grades:
            return f"No grades found for {subject_name} to base a prediction on."
            
        current_weighted_score = sum(g.score * (g.assessment.weight / 100) for g in grades)
        current_total_weight = sum(g.assessment.weight for g in grades)
        
        # Normalize current score to 100 scale for the function if needed, 
        # but logic.predict_grade_needed takes current_score as raw average? 
        # Actually logic.predict_grade_needed logic is a bit specific.
        # Let's use the weighted sum directly.
        
        # If we have 60% of the course done, and we have 50 points so far.
        # We need X points in the remaining 40%.
        # Target for A is 90 points total.
        # 90 - 50 = 40 needed.
        # 40 points out of 40% weight = 100% score needed.
        
        target_score = 0
        if target_grade == "A": target_score = 90
        elif target_grade == "B": target_score = 80
        elif target_grade == "C": target_score = 70
        elif target_grade == "D": target_score = 60
        
        needed_points = target_score - current_weighted_score
        remaining_weight = 100 - current_total_weight
        
        if remaining_weight <= 0:
             return "You have completed all assessments for this course."
             
        required_avg_on_remainder = (needed_points / remaining_weight) * 100
        
        if required_avg_on_remainder > 100:
            return f"It's effectively impossible. You'd need {required_avg_on_remainder:.1f}% on remaining work."
        elif required_avg_on_remainder < 0:
            return "You've already secured that grade!"
        else:
            return f"You need to average {required_avg_on_remainder:.1f}% on the remaining {remaining_weight}% of the course."

    return "I'm not sure I understand. Try asking about your grades in a specific subject or your overall performance."
