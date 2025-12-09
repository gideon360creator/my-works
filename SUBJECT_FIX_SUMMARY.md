# Subject Visibility Fix - Summary

## Problem
When lecturers added new subjects, students couldn't see them without manually refreshing the browser page.

## Root Cause
The student Dashboard component (`Dashboard.jsx`) only fetched subjects once when the page loaded. There was no mechanism to check for updates.

## Solution Implemented

### 1. Auto-Refresh Feature
- Added automatic data refresh every 30 seconds
- Runs in the background using `setInterval`
- Properly cleaned up when component unmounts

### 2. Manual Refresh Button
- Added a "Refresh" button in the header
- Shows spinning animation while loading
- Allows students to immediately see new subjects without waiting

## Code Changes

### File: `frontend/src/pages/Dashboard.jsx`

**Added:**
- `refreshing` state to track manual refresh status
- `fetchData()` function extracted from useEffect
- Auto-refresh interval (30 seconds)
- Manual refresh button with loading state

**Benefits:**
- ✅ Students see new subjects within 30 seconds automatically
- ✅ Students can manually refresh for immediate updates
- ✅ No full page reload required
- ✅ Smooth user experience with loading indicators

## Testing Instructions

1. **Start the backend server** (if not running):
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   ```

2. **Start the frontend** (if not running):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test the fix:**
   - Login as a lecturer
   - Go to "Manage Grades" tab
   - Add a new subject (e.g., "Biology", "BIO101")
   - Login as a student (in another browser/incognito)
   - Wait up to 30 seconds OR click the "Refresh" button
   - The new subject should now appear!

## Backend Verification
The backend code was already correct:
- ✅ `db.commit()` properly saves subjects
- ✅ GET `/subjects/` endpoint works correctly
- ✅ No caching issues

No backend changes were needed.

### 3. GPA (5-point) & Live Calculation

We added a small feature to calculate student GPA on a 5-point scale and to make the GPA update live based on the scores that are currently available.

What changed:
- Backend (`backend/logic.py`): Replaced the previous 4.0 mapping with a function that computes a percentage per recorded grade (uses `assessment.max_score` if available), builds a weighted average using assessment `weight` values when present, falls back to a simple average when weights aren't available, and scales the final percentage to a 5-point GPA using `gpa5 = (percentage / 100) * 5`. The function returns a float rounded to two decimals.
- Frontend (`frontend/src/pages/Dashboard.jsx`): Replaced the old discrete 4.0 mapping with a live calculation (`computeFivePointGPA`) that mirrors the backend logic: it computes per-grade percentages, applies assessment weights when available, blends unweighted grades conservatively, and displays the resulting 5-point GPA with two decimals in the dashboard UI.

Why this approach:
- "Live" means the GPA uses only recorded grades so far; as new grades are entered the GPA will update automatically (the dashboard auto-refreshes every 30s and has a manual Refresh button).
- Using percentage -> 5.0 scaling gives a continuous GPA that's sensitive to partial progress (e.g., a current course average of 80% maps to 4.0 on the 5-point scale).

Testing steps (quick):
1. Start backend and frontend as described in the previous section.
2. Create assessments with `max_score` and `weight` (weights are percentages, e.g., 30 for 30%).
3. Add grades for a student. Observe the GPA on the student Dashboard update after a refresh (or wait up to 30s for auto-refresh).
4. Try mixtures of weighted and unweighted scores to confirm graceful fallbacks.

Notes & next improvements:
- If you prefer a discrete letter->point mapping (e.g., A=5, B=4, C=3, D=2, F=0), I can change both backend and frontend to that mapping instead.
- We can add a dedicated endpoint `/grades/me/gpa` that returns the GPA and breakdown (final percentage, total recorded weight, count of graded assessments) for easier client consumption.
- I can add unit tests for `calculate_gpa` (backend) and a small component test for the frontend calculation.
