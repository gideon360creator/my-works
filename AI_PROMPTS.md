# AI Chatbot Prompts — Cheat Sheet

This file lists example prompts and templates that the app's AI chatbot understands well. Use or adapt these in the chat UI. Grouped by purpose with copy-ready templates and tips.

---

## Student queries (grade lookups)
- What is my current grade in Mathematics (MATH101)?
- Show my grades for assessments in Computer Science this semester.
- What was my score on Assessment #12 and how does that affect my average?
- What is my GPA and how was it calculated?
- Which of my assessments are missing scores?
- Give me a breakdown of my performance in [subject name or code] by assessment type (exam, assignment, quiz).
- List my most recent 5 graded assessments and their scores.

Templates:
- "What is my grade in [SUBJECT_NAME or SUBJECT_CODE]?"
- "Show my grades for [SUBJECT_CODE] this semester."

---

## Prediction & Planning
- How many marks do I need on the final exam to reach a 70% course average in MATH101?
- If I get 85% on Assignment 3, what will my overall grade be in CS101?

Template:
- "If I get [SCORE]% on [ASSESSMENT_NAME], what will be my final course average in [SUBJECT]?"

---

## Study & improvement help
- I scored 58% on the physics midterm — suggest a 4-week study plan to raise it to 75%.
- Explain the main topics I should review for MATH101 final exam and give practice problem ideas.
- Create a weekly study schedule (6 weeks) to prepare for Finals in Computer Science.
- Recommend resources (videos, books, exercises) for learning calculus integration techniques.

Template:
- "Create a [WEEKS]-week study plan to reach [TARGET]% in [COURSE_NAME]."

---

## Lecturer / admin prompts
- Show average score and standard deviation for Assessment #7 (Data Structures).
- Which students are at risk (average < 50%) in CS101? List username and current average.
- Give me class-wide grade distribution (A/B/C/D/F) for last semester’s final exam.
- Suggest reweighting schemes to improve fairness if many students missed the midterm.
- Provide a short feedback template I can send to students scoring below 40%.

Template:
- "Summarize performance for [SUBJECT_CODE] assessment [ASSESSMENT_ID] — show average, median, stdev, and percent below 50%."

---

## Assessment creation & grading help
- What weightings should I use for assignments/midterm/final to reflect a 40/30/30 split?
- Create a rubric for grading lab reports (out of 100) with clear criteria.
- Generate sample exam questions for [topic], 3 easy, 4 medium, 3 hard.

Template:
- "Create a rubric for [ASSESSMENT_TYPE] out of [MAX_SCORE] with criteria and weightings."

---

## Chatbot & app help (meta)
- How do I register and log in using my matriculation number?
- How can I update my password?
- What does this error mean: 'Incorrect username or password'?
- How do I manage grades as a lecturer in the app?

---

## Fallback & clarification prompts (if the bot can't find something)
- "I meant [SUBJECT NAME or CODE]."
- "List subjects that match '[TERM]'"
- "Show the available subjects and their codes."

These help the bot disambiguate when it can't locate a subject or assessment.

---

## Quick tips for better responses
- Be specific: include subject code or assessment name/ID when possible (e.g., "MATH101" or "Midterm Exam").
- Provide numbers where possible (target percent, current scores) when asking prediction questions.
- Ask follow-ups: after a high-level answer, request a plan, resources, or examples.
- For step-by-step solutions, add "Show step-by-step" or "Explain in detail".

---

## Example full sessions
1) Student grade check + improvement:
- "What is my current grade in MATH101?"
- Bot responds with current grades and weighted score.
- Student: "If I get 80% on the final (40% weight), what will my overall grade be?"

2) Lecturer analytics:
- "Show grade distribution for CS101 final exam."
- Bot: distribution + percentiles.
- Lecturer: "List students below 50%." -> bot returns list.

---

## Extending prompts and templates
To add more canned prompts in the UI, provide short, actionable phrases such as:
- "My GPA"
- "Recent grades"
- "Study plan for MATH101"

These make good quick-reply buttons in the chat UI.

---

## File info
This document is intended to be a living cheat-sheet. Update it when you add new chatbot features or endpoints.

