from sqlalchemy.orm import Session
import models

def calculate_grade_letter(score: float) -> str:
    if score >= 90: return "A"
    elif score >= 80: return "B"
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    else: return "F"

def calculate_gpa(grades: list[models.Grade]) -> float:
    """
    Calculate a GPA on a 5-point scale using only available (recorded) scores.

    Approach / assumptions:
    - Each Grade links to an Assessment which has a `max_score` and a `weight` (percentage of final course).
    - We compute the percentage for each recorded grade as (grade.score / assessment.max_score) * 100
      if `max_score` is available; otherwise we treat `grade.score` as a percentage already.
    - We compute a weighted average percentage using only assessments that have recorded grades, where
      each assessment contributes according to its `weight`.
    - If no weights are available (sum of weights == 0) we fall back to a simple average of percentages.
    - Finally we scale the resulting percentage to a 5-point GPA by: gpa5 = (percentage / 100) * 5.

    Returns the GPA as a float rounded to 2 decimal places.
    """
    if not grades:
        return 0.0

    total_weighted_percentage = 0.0
    total_weight = 0.0
    percentages = []

    for grade in grades:
        try:
            assessment = grade.assessment
        except Exception:
            assessment = None

        # Compute percentage for this grade
        if assessment and assessment.max_score and assessment.max_score > 0:
            pct = (grade.score / assessment.max_score) * 100
        else:
            # Assume score already a percentage
            pct = grade.score

        # If assessment provides a weight, use it; otherwise treat as unweighted entry
        weight = assessment.weight if (assessment and getattr(assessment, 'weight', None) is not None) else 0.0

        if weight and weight > 0:
            total_weighted_percentage += pct * weight
            total_weight += weight
        else:
            # Save as unweighted percentage entry for fallback averaging
            percentages.append(pct)

    final_percentage = 0.0
    if total_weight > 0:
        # Weighted average across graded assessments (weights are percentages, e.g., 30.0)
        final_percentage = total_weighted_percentage / total_weight
        # If there are also unweighted percentage entries, blend them equally into the average
        if len(percentages) > 0:
            # simple average of the unweighted percentages
            avg_unweighted = sum(percentages) / len(percentages)
            # Blend by giving the unweighted block an equivalent weight equal to the average of weights
            avg_weight = total_weight / (len(percentages) + 1) if len(percentages) > 0 else total_weight
            # A conservative approach: take mean of weighted average and avg_unweighted
            final_percentage = (final_percentage + avg_unweighted) / 2
    else:
        # No weight information present; fall back to simple average of all percentages
        all_pcts = percentages + ([] if total_weight == 0 else [])
        if len(all_pcts) == 0:
            return 0.0
        final_percentage = sum(all_pcts) / len(all_pcts)

    # Scale percentage (0-100) to 5-point scale
    gpa5 = (final_percentage / 100.0) * 5.0
    return round(gpa5, 2)


def calculate_gpa_breakdown(grades: list[models.Grade]) -> dict:
    """
    Return a breakdown useful for an API response:
    {
        'gpa': float,            # 5-point GPA
        'percentage': float,     # underlying percentage average (0-100)
        'recorded_weight': float,# sum of weights used in calculation
        'graded_assessments': int# number of graded assessments considered
    }
    """
    if not grades:
        return {
            'gpa': 0.0,
            'percentage': 0.0,
            'recorded_weight': 0.0,
            'graded_assessments': 0
        }

    total_weighted_percentage = 0.0
    total_weight = 0.0
    percentages = []
    graded_count = 0

    for grade in grades:
        graded_count += 1
        try:
            assessment = grade.assessment
        except Exception:
            assessment = None

        if assessment and assessment.max_score and assessment.max_score > 0:
            pct = (grade.score / assessment.max_score) * 100
        else:
            pct = grade.score

        weight = assessment.weight if (assessment and getattr(assessment, 'weight', None) is not None) else 0.0

        if weight and weight > 0:
            total_weighted_percentage += pct * weight
            total_weight += weight
        else:
            percentages.append(pct)

    if total_weight > 0:
        final_percentage = total_weighted_percentage / total_weight
        if len(percentages) > 0:
            avg_unweighted = sum(percentages) / len(percentages)
            final_percentage = (final_percentage + avg_unweighted) / 2
    else:
        all_pcts = percentages
        if len(all_pcts) == 0:
            final_percentage = 0.0
        else:
            final_percentage = sum(all_pcts) / len(all_pcts)

    gpa5 = (final_percentage / 100.0) * 5.0
    return {
        'gpa': round(gpa5, 2),
        'percentage': round(final_percentage, 2),
        'recorded_weight': round(total_weight, 2),
        'graded_assessments': graded_count
    }

def get_student_performance_summary(db: Session, student_id: int):
    grades = db.query(models.Grade).filter(models.Grade.student_id == student_id).all()
    if not grades:
        return "No grades recorded yet."
    
    gpa = calculate_gpa(grades)
    total_subjects = len(grades)
    
    # Identify strengths and weaknesses
    sorted_grades = sorted(grades, key=lambda g: g.score, reverse=True)
    best_subject = sorted_grades[0].assessment.subject.name if sorted_grades else "N/A"
    worst_subject = sorted_grades[-1].assessment.subject.name if sorted_grades else "N/A"
    
    return {
        "gpa": gpa,
        "total_subjects": total_subjects,
        "best_subject": best_subject,
        "worst_subject": worst_subject,
        "summary": f"Current GPA is {gpa}. Best performance in {best_subject}."
    }

def predict_grade_needed(current_score: float, current_weight: float, target_grade_letter: str) -> str:
    # Simplified prediction: "What do I need on the final (remaining weight) to get X?"
    # This requires more complex logic about total course structure, 
    # assuming we know the total weight is 100.
    
    target_score = 0
    if target_grade_letter == "A": target_score = 90
    elif target_grade_letter == "B": target_score = 80
    elif target_grade_letter == "C": target_score = 70
    elif target_grade_letter == "D": target_score = 60
    
    remaining_weight = 100 - current_weight
    if remaining_weight <= 0:
        return "Course is already completed or weights are incorrect."
        
    # Formula: (CurrentScore * CurrentWeight + NeededScore * RemainingWeight) / 100 = TargetScore
    # NeededScore = (TargetScore * 100 - CurrentScore * CurrentWeight) / RemainingWeight
    
    needed_score = (target_score * 100 - current_score * current_weight) / remaining_weight
    
    if needed_score > 100:
        return "It is mathematically impossible to achieve this grade."
    elif needed_score < 0:
        return "You have already secured this grade."
    else:
        return f"You need to score at least {needed_score:.1f}% on the remaining assessments."
