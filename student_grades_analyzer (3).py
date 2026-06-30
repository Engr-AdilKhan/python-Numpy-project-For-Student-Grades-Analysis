"""
================================================================================
STUDENT GRADES ANALYZER — A Beginner NumPy Project
================================================================================
WHAT THIS PROJECT DOES:
    Imagine a class of students who each took 5 subject exams.
    This program uses NumPy to:
        1. Store all the marks in a single array (a grid of numbers)
        2. Calculate each student's average and total marks
        3. Find the topper (highest average) and the student who needs help
        4. Calculate the class average for each subject
        5. Find the hardest and easiest subject (based on average marks)
        6. Assign letter grades (A/B/C/D/F) to every student automatically
        7. Mark every student as PASS or FAIL
        8. Print a clean, nicely formatted report card for the whole class

    No charts, no images — just clear, well-decorated console output.

WHY NUMPY (instead of plain Python lists)?
    NumPy lets us treat the entire grid of marks as ONE object and run
    calculations on it instantly — no manual loops needed to add up numbers
    or find averages. This is called "vectorization", and it's the main
    reason NumPy is used everywhere in data science.

HOW TO RUN:
    pip install numpy
    python student_grades_analyzer.py
================================================================================
"""

import numpy as np

# ------------------------------------------------------------------------------
# SMALL HELPER FUNCTIONS — just for making the console output look nicer
# (these are plain Python, not NumPy, but they make the report readable)
# ------------------------------------------------------------------------------

def print_title(text):
    """Prints a big boxed title."""
    width = 70
    print("\n╔" + "═" * (width - 2) + "╗")
    print("║" + text.center(width - 2) + "║")
    print("╚" + "═" * (width - 2) + "╝")


def print_section(text):
    """Prints a section header."""
    width = 70
    print("\n┌" + "─" * (width - 2) + "┐")
    print("│ " + text.ljust(width - 3) + "│")
    print("└" + "─" * (width - 2) + "┘")


def print_table(headers, rows, col_widths):
    """Prints a clean table with borders, given headers and row data."""
    # Top border
    border = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    print(border)

    # Header row
    header_row = "|"
    for h, w in zip(headers, col_widths):
        header_row += f" {h:^{w}} |"
    print(header_row)
    print(border)

    # Data rows
    for row in rows:
        row_str = "|"
        for cell, w in zip(row, col_widths):
            row_str += f" {str(cell):^{w}} |"
        print(row_str)
    print(border)


# ------------------------------------------------------------------------------
# STEP 1: CREATE THE DATA
# ------------------------------------------------------------------------------
# 20 students, each took 5 subject exams (marks out of 100):
# Math, Science, English, History, Computer Science
#
# Since typing 20 students' marks by hand would be tedious, we use NumPy's
# random number generator to create realistic-looking marks instead.
# np.random.seed(42) makes sure you get the SAME "random" numbers every time
# you run this file — this is important for reproducibility.

np.random.seed(42)

student_names = [
    "Ali", "Sara", "Bilal", "Fatima", "Usman", "Ayesha", "Hassan", "Zara",
    "Omar", "Mariam", "Talha", "Hira", "Faizan", "Noor", "Kashif", "Sana",
    "Imran", "Laiba", "Adeel", "Rabia"
]
subjects = ["Math", "Science", "English", "History", "Computer Science"]

# np.random.randint(low, high, size) creates random whole numbers between
# low (inclusive) and high (exclusive). Here we generate marks between
# 30 and 100 for 20 students x 5 subjects -> a (20, 5) shaped array.
marks = np.random.randint(30, 101, size=(len(student_names), len(subjects)))

print_title("📊  STUDENT GRADES ANALYZER  📊")

print(f"\n  Students : {marks.shape[0]}")   # shape[0] = number of rows
print(f"  Subjects : {marks.shape[1]}")     # shape[1] = number of columns

print_section("RAW MARKS TABLE")
raw_rows = [[student_names[i]] + list(marks[i]) for i in range(len(student_names))]
print_table(["Student"] + subjects, raw_rows, [8, 5, 8, 8, 8, 18])


# ------------------------------------------------------------------------------
# STEP 2: CALCULATE EACH STUDENT'S AVERAGE AND TOTAL
# ------------------------------------------------------------------------------
# axis=1 means "go across each row" (i.e., across all subjects for one student)
# This single line replaces what would normally be a 5-line loop in plain Python!

student_totals = marks.sum(axis=1)     # total marks per student
student_averages = marks.mean(axis=1)  # average marks per student

print_section("STEP 2: Per-Student Totals & Averages")
rows = [[student_names[i], student_totals[i], f"{student_averages[i]:.1f}"]
        for i in range(len(student_names))]
print_table(["Student", "Total / 500", "Average"], rows, [10, 12, 10])


# ------------------------------------------------------------------------------
# STEP 3: FIND THE TOPPER AND THE WEAKEST STUDENT
# ------------------------------------------------------------------------------
# np.argmax() and np.argmin() return the INDEX (position) of the
# highest/lowest value, not the value itself. We use that index to
# look up the student's name.

topper_index = np.argmax(student_averages)
weakest_index = np.argmin(student_averages)

print_section("STEP 3: Class Topper & Student Who Needs Help")
print(f"  🏆  Topper           : {student_names[topper_index]} "
      f"(Average: {student_averages[topper_index]:.1f})")
print(f"  📌  Needs most help  : {student_names[weakest_index]} "
      f"(Average: {student_averages[weakest_index]:.1f})")


# ------------------------------------------------------------------------------
# STEP 4: CALCULATE CLASS AVERAGE PER SUBJECT
# ------------------------------------------------------------------------------
# axis=0 means "go down each column" (i.e., across all students for one subject)
# Notice: axis=1 was "across a row", axis=0 is "down a column" — this is the
# single most confusing-but-important concept in NumPy, so pay attention here!

subject_averages = marks.mean(axis=0)

print_section("STEP 4: Class Average Per Subject")
rows = [[subjects[i], f"{subject_averages[i]:.1f}"] for i in range(len(subjects))]
print_table(["Subject", "Class Average"], rows, [20, 14])

hardest_subject_index = np.argmin(subject_averages)
easiest_subject_index = np.argmax(subject_averages)

print(f"\n  📉  Hardest subject (lowest average)  : {subjects[hardest_subject_index]}")
print(f"  📈  Easiest subject (highest average) : {subjects[easiest_subject_index]}")


# ------------------------------------------------------------------------------
# STEP 5: ASSIGN LETTER GRADES AUTOMATICALLY
# ------------------------------------------------------------------------------
# Here we use a NumPy feature called "boolean masking" + np.select().
# Instead of writing if/elif/else for every single student in a loop,
# we describe the RULES once, and NumPy applies them to the whole array
# of averages all at once.

conditions = [
    student_averages >= 90,                                     # A
    (student_averages >= 75) & (student_averages < 90),          # B
    (student_averages >= 60) & (student_averages < 75),          # C
    (student_averages >= 40) & (student_averages < 60),          # D
    student_averages < 40                                         # F
]
grade_labels = ["A", "B", "C", "D", "F"]

letter_grades = np.select(conditions, grade_labels, default="F")

# We can also use a simple boolean condition to mark each student as
# PASS or FAIL (here, passing means average >= 40). np.where() checks
# the condition for every student at once and picks the right label.
pass_fail_status = np.where(student_averages >= 40, "PASS ✅", "FAIL ❌")

print_section("STEP 5: Automatic Letter Grades")
rows = [[student_names[i], f"{student_averages[i]:.1f}", letter_grades[i]]
        for i in range(len(student_names))]
print_table(["Student", "Average", "Grade"], rows, [10, 10, 7])


# ------------------------------------------------------------------------------
# STEP 6: A FEW MORE USEFUL NUMPY STATS (just to show what's possible)
# ------------------------------------------------------------------------------
passed = np.sum(student_averages >= 40)   # counts how many "True" values
failed = np.sum(student_averages < 40)

print_section("STEP 6: Extra Class Statistics")
print(f"  🔼  Highest single mark in the class : {marks.max()}")
print(f"  🔽  Lowest single mark in the class  : {marks.min()}")
print(f"  📊  Overall class average            : {marks.mean():.1f}")
print(f"  📐  Standard deviation of all marks  : {marks.std():.1f}  (how spread out the marks are)")
print(f"  ✅  Students passed                  : {passed} / {len(student_names)}")
print(f"  ❌  Students failed                  : {failed} / {len(student_names)}")


# ------------------------------------------------------------------------------
# FINAL REPORT CARD
# ------------------------------------------------------------------------------
print_title("🎓  FINAL REPORT CARD  🎓")

final_rows = [
    [student_names[i], student_totals[i], f"{student_averages[i]:.1f}",
     letter_grades[i], pass_fail_status[i]]
    for i in range(len(student_names))
]
print_table(
    ["Student", "Total", "Average", "Grade", "Status"],
    final_rows,
    [10, 7, 9, 7, 10]
)

print("\n✨ Done! This whole analysis was done using NumPy arrays —")
print("   no manual loops were needed to calculate totals, averages, or grades.\n")
