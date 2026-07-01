# ============================================================
# Student Performance Management and Data Analysis System
# Part 1 (Updated)
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

FILE_NAME = "students.csv"

# ============================================================
# Student Class
# ============================================================

class Student:

    def __init__(self, sid, name, age, gender):

        self.sid = sid
        self.name = name
        self.age = age
        self.gender = gender

        self.math = 0
        self.physics = 0
        self.chemistry = 0
        self.english = 0
        self.computer = 0

        self.total = 0
        self.percentage = 0
        self.grade = ""

    # ========================================================
    # Enter Marks from User
    # ========================================================

    def generate_marks(self):

        print("\nEnter Student Marks (0 - 100)")

        while True:
            self.math = float(input("Math       : "))
            if 0 <= self.math <= 100:
                break
            print("Marks must be between 0 and 100.")

        while True:
            self.physics = float(input("Physics    : "))
            if 0 <= self.physics <= 100:
                break
            print("Marks must be between 0 and 100.")

        while True:
            self.chemistry = float(input("Chemistry  : "))
            if 0 <= self.chemistry <= 100:
                break
            print("Marks must be between 0 and 100.")

        while True:
            self.english = float(input("English    : "))
            if 0 <= self.english <= 100:
                break
            print("Marks must be between 0 and 100.")

        while True:
            self.computer = float(input("Computer   : "))
            if 0 <= self.computer <= 100:
                break
            print("Marks must be between 0 and 100.")

        self.calculate_result()

    # ========================================================
    # Calculate Total, Percentage and Grade
    # ========================================================

    def calculate_result(self):

        self.total = (
            self.math +
            self.physics +
            self.chemistry +
            self.english +
            self.computer
        )

        self.percentage = self.total / 5

        if self.percentage >= 90:
            self.grade = "A+"

        elif self.percentage >= 80:
            self.grade = "A"

        elif self.percentage >= 70:
            self.grade = "B"

        elif self.percentage >= 60:
            self.grade = "C"

        elif self.percentage >= 50:
            self.grade = "D"

        else:
            self.grade = "Fail"

    # ========================================================
    # Convert Object into List
    # ========================================================

    def to_list(self):

        return [
            self.sid,
            self.name,
            self.age,
            self.gender,
            self.math,
            self.physics,
            self.chemistry,
            self.english,
            self.computer,
            self.total,
            self.percentage,
            self.grade
        ]

# ============================================================
# Result Class (Inheritance)
# ============================================================

class Result(Student):

    def __init__(self, sid, name, age, gender):
        super().__init__(sid, name, age, gender)

    def display(self):

        print("\n" + "=" * 60)
        print("STUDENT RESULT")
        print("=" * 60)

        print(f"ID         : {self.sid}")
        print(f"Name       : {self.name}")
        print(f"Age        : {self.age}")
        print(f"Gender     : {self.gender}")

        print("-" * 60)

        print(f"Math       : {self.math}")
        print(f"Physics    : {self.physics}")
        print(f"Chemistry  : {self.chemistry}")
        print(f"English    : {self.english}")
        print(f"Computer   : {self.computer}")

        print("-" * 60)

        print(f"Total      : {self.total}")
        print(f"Percentage : {self.percentage:.2f}")
        print(f"Grade      : {self.grade}")

        print("=" * 60)


# ============================================================
# Create CSV Database
# ============================================================

def create_database():

    if not os.path.exists(FILE_NAME):

        columns = [
            "ID",
            "Name",
            "Age",
            "Gender",
            "Math",
            "Physics",
            "Chemistry",
            "English",
            "Computer",
            "Total",
            "Percentage",
            "Grade"
        ]

        df = pd.DataFrame(columns=columns)

        df.to_csv(FILE_NAME, index=False)

        print("Database Created Successfully")

    else:

        print("Database Already Exists")


# ============================================================
# Add Student
# ============================================================

def add_student():

    sid = input("Enter Student ID : ")
    name = input("Enter Student Name : ")
    age = int(input("Enter Age : "))
    gender = input("Enter Gender : ")

    student = Result(sid, name, age, gender)

    student.generate_marks()

    df = pd.read_csv(FILE_NAME)

    df.loc[len(df)] = student.to_list()

    df.to_csv(FILE_NAME, index=False)

    print("\nStudent Added Successfully.")
    # ============================================================
# Display All Students
# ============================================================

def display_students():

    try:

        df = pd.read_csv(FILE_NAME)

        if df.empty:
            print("\nNo Student Records Found.")
            return

        print("\n")
        print("=" * 100)
        print(df)
        print("=" * 100)

    except FileNotFoundError:
        print("Database File Not Found.")


# ============================================================
# Search Student
# ============================================================

def search_student():

    sid = input("Enter Student ID : ")

    try:

        df = pd.read_csv(FILE_NAME)

        result = df[df["ID"].astype(str) == sid]

        if result.empty:
            print("\nStudent Not Found")

        else:
            print("\nStudent Found\n")
            print(result)

    except FileNotFoundError:
        print("Database File Not Found")


# ============================================================
# Delete Student
# ============================================================

def delete_student():

    sid = input("Enter Student ID : ")

    try:

        df = pd.read_csv(FILE_NAME)

        if sid not in df["ID"].astype(str).values:

            print("Student Not Found")
            return

        df = df[df["ID"].astype(str) != sid]

        df.to_csv(FILE_NAME, index=False)

        print("Student Deleted Successfully")

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Update Student Information
# ============================================================

def update_student():

    sid = input("Enter Student ID : ")

    try:

        df = pd.read_csv(FILE_NAME)

        if sid not in df["ID"].astype(str).values:

            print("Student Not Found")
            return

        index = df[df["ID"].astype(str) == sid].index[0]

        print("\nLeave Blank to Keep Old Value\n")

        name = input("New Name : ")
        age = input("New Age : ")
        gender = input("New Gender : ")

        if name != "":
            df.at[index, "Name"] = name

        if age != "":
            df.at[index, "Age"] = int(age)

        if gender != "":
            df.at[index, "Gender"] = gender

        df.to_csv(FILE_NAME, index=False)

        print("Student Updated Successfully")

    except FileNotFoundError:

        print("Database File Not Found")

# ============================================================
# Display Complete Result of One Student
# ============================================================

def view_result():

    sid = input("Enter Student ID : ")

    try:

        df = pd.read_csv(FILE_NAME)

        student = df[df["ID"].astype(str) == sid]

        if student.empty:

            print("Student Not Found")
            return

        print("\n")
        print("=" * 70)

        print("STUDENT RESULT")

        print("=" * 70)

        row = student.iloc[0]

        print("ID          :", row["ID"])
        print("Name        :", row["Name"])
        print("Age         :", row["Age"])
        print("Gender      :", row["Gender"])

        print("-" * 70)

        print("Math        :", row["Math"])
        print("Physics     :", row["Physics"])
        print("Chemistry   :", row["Chemistry"])
        print("English     :", row["English"])
        print("Computer    :", row["Computer"])

        print("-" * 70)

        print("Total       :", row["Total"])
        print("Percentage  :", round(row["Percentage"],2))
        print("Grade       :", row["Grade"])

        print("=" * 70)

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Overall Statistics
# ============================================================

def statistics():

    df = pd.read_csv(FILE_NAME)

    print("\n========== OVERALL STATISTICS ==========\n")

    print("Total Students      :", len(df))
    print("Highest Percentage  :", df["Percentage"].max())
    print("Lowest Percentage   :", df["Percentage"].min())
    print("Average Percentage  :", round(df["Percentage"].mean(),2))
    print("Highest Total Marks :", df["Total"].max())
    print("Lowest Total Marks  :", df["Total"].min())


# ============================================================
# Topper
# ============================================================

def topper():

    df = pd.read_csv(FILE_NAME)

    top = df.sort_values(
        by="Percentage",
        ascending=False
    )

    print("\nTOPPER\n")

    print(top.head(1))


# ============================================================
# Lowest Scorer
# ============================================================

def lowest_student():

    df = pd.read_csv(FILE_NAME)

    low = df.sort_values(
        by="Percentage"
    )

    print("\nLOWEST SCORER\n")

    print(low.head(1))


# ============================================================
# Grade Report
# ============================================================

def grade_report():

    df = pd.read_csv(FILE_NAME)

    print("\nGRADE REPORT\n")

    grades = df["Grade"].value_counts()

    print(grades)

# ============================================================
# Subject Wise Analysis
# ============================================================

def subject_analysis():

    try:

        df = pd.read_csv(FILE_NAME)

        subjects = [
            "Math",
            "Physics",
            "Chemistry",
            "English",
            "Computer"
        ]

        print("\n========== SUBJECT ANALYSIS ==========\n")

        for subject in subjects:

            print(f"{subject}")

            print("Highest :", df[subject].max())
            print("Lowest  :", df[subject].min())
            print("Average :", round(df[subject].mean(), 2))

            print("-" * 40)

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# NumPy Statistical Analysis
# ============================================================

def numpy_analysis():

    try:

        df = pd.read_csv(FILE_NAME)

        marks = df[
            [
                "Math",
                "Physics",
                "Chemistry",
                "English",
                "Computer"
            ]
        ].to_numpy()

        print("\n========== NUMPY ANALYSIS ==========\n")

        print("Shape")
        print(marks.shape)

        print("\nMaximum Marks")
        print(np.max(marks))

        print("\nMinimum Marks")
        print(np.min(marks))

        print("\nMean")
        print(np.mean(marks))

        print("\nMedian")
        print(np.median(marks))

        print("\nStandard Deviation")
        print(np.std(marks))

        print("\nVariance")
        print(np.var(marks))

        print("\nColumn Wise Average")
        print(np.mean(marks, axis=0))

        print("\nStudent Wise Average")
        print(np.mean(marks, axis=1))

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Generate Random Students
# ============================================================

def random_students():

    total = int(input("Enter Number of Students : "))

    names = [
        "Ali", "Ahmed", "Usman", "Bilal", "Hamza",
        "Sara", "Ayesha", "Fatima", "Noor", "Maryam",
        "Hassan", "Zain", "Amir", "Asad", "Saad"
    ]

    genders = ["Male", "Female"]

    df = pd.read_csv(FILE_NAME)

    for i in range(total):

        sid = np.random.randint(1000, 9999)

        name = np.random.choice(names)

        age = np.random.randint(18, 26)

        gender = np.random.choice(genders)

        student = Result(sid, name, age, gender)

        student.generate_marks()

        df.loc[len(df)] = student.to_list()

    df.to_csv(FILE_NAME, index=False)

    print(f"\n{total} Students Added Successfully.")

# ============================================================
# Backup Database
# ============================================================

def backup_database():

    try:

        df = pd.read_csv(FILE_NAME)

        backup_file = "students_backup.csv"

        df.to_csv(backup_file, index=False)

        print("\nBackup Created Successfully.")
        print("Backup File :", backup_file)

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Export Top Students
# ============================================================

def export_top_students():

    try:

        df = pd.read_csv(FILE_NAME)

        top = df.sort_values(
            by="Percentage",
            ascending=False
        )

        top10 = top.head(10)

        top10.to_csv("top_students.csv", index=False)

        print("\nTop 10 Students Exported Successfully.")

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Matplotlib Bar Chart
# ============================================================

def bar_chart():

    df = pd.read_csv(FILE_NAME)

    plt.figure(figsize=(10,6))

    plt.bar(
        df["Name"],
        df["Percentage"]
    )

    plt.title("Student Percentage")

    plt.xlabel("Students")

    plt.ylabel("Percentage")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


# ============================================================
# Matplotlib Line Chart
# ============================================================

def line_chart():

    df = pd.read_csv(FILE_NAME)

    plt.figure(figsize=(10,6))

    plt.plot(
        df["Name"],
        df["Percentage"],
        marker="o"
    )

    plt.title("Percentage Line Chart")

    plt.xlabel("Students")

    plt.ylabel("Percentage")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


# ============================================================
# Matplotlib Histogram
# ============================================================

def histogram():

    df = pd.read_csv(FILE_NAME)

    plt.figure(figsize=(8,5))

    plt.hist(
        df["Percentage"],
        bins=10
    )

    plt.title("Percentage Distribution")

    plt.xlabel("Percentage")

    plt.ylabel("Frequency")

    plt.show()

# ============================================================
# Matplotlib Pie Chart
# ============================================================

def pie_chart():

    try:

        df = pd.read_csv(FILE_NAME)

        grade_count = df["Grade"].value_counts()

        plt.figure(figsize=(8,8))

        plt.pie(
            grade_count.values,
            labels=grade_count.index,
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Grade Distribution")

        plt.show()

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Matplotlib Scatter Plot
# ============================================================

def scatter_chart():

    try:

        df = pd.read_csv(FILE_NAME)

        plt.figure(figsize=(8,6))

        plt.scatter(
            df["Math"],
            df["Computer"]
        )

        plt.title("Math vs Computer Marks")

        plt.xlabel("Math")

        plt.ylabel("Computer")

        plt.grid(True)

        plt.show()

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Matplotlib Box Plot
# ============================================================

def box_chart():

    try:

        df = pd.read_csv(FILE_NAME)

        plt.figure(figsize=(8,6))

        plt.boxplot(
            [
                df["Math"],
                df["Physics"],
                df["Chemistry"],
                df["English"],
                df["Computer"]
            ],
            labels=[
                "Math",
                "Physics",
                "Chemistry",
                "English",
                "Computer"
            ]
        )

        plt.title("Subject Wise Marks")

        plt.ylabel("Marks")

        plt.show()

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Seaborn Count Plot
# ============================================================

def count_plot():

    try:

        df = pd.read_csv(FILE_NAME)

        plt.figure(figsize=(7,5))

        sns.countplot(
            data=df,
            x="Grade"
        )

        plt.title("Students by Grade")

        plt.show()

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Seaborn Box Plot
# ============================================================

def seaborn_boxplot():

    try:

        df = pd.read_csv(FILE_NAME)

        plt.figure(figsize=(8,6))

        sns.boxplot(
            data=df[
                [
                    "Math",
                    "Physics",
                    "Chemistry",
                    "English",
                    "Computer"
                ]
            ]
        )

        plt.title("Subject Wise Box Plot")

        plt.show()

    except FileNotFoundError:

        print("Database File Not Found")

# ============================================================
# Seaborn Violin Plot
# ============================================================

def violin_plot():

    try:

        df = pd.read_csv(FILE_NAME)

        plt.figure(figsize=(10,6))

        sns.violinplot(
            data=df[
                [
                    "Math",
                    "Physics",
                    "Chemistry",
                    "English",
                    "Computer"
                ]
            ]
        )

        plt.title("Subject Wise Marks Distribution")

        plt.show()

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Seaborn Heatmap
# ============================================================

def heatmap_chart():

    try:

        df = pd.read_csv(FILE_NAME)

        corr = df[
            [
                "Math",
                "Physics",
                "Chemistry",
                "English",
                "Computer",
                "Percentage"
            ]
        ].corr()

        plt.figure(figsize=(8,6))

        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm"
        )

        plt.title("Correlation Heatmap")

        plt.show()

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Seaborn Pair Plot
# ============================================================

def pair_plot():

    try:

        df = pd.read_csv(FILE_NAME)

        sns.pairplot(
            df[
                [
                    "Math",
                    "Physics",
                    "Chemistry",
                    "English",
                    "Computer"
                ]
            ]
        )

        plt.show()

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Student Ranking
# ============================================================

def ranking():

    try:

        df = pd.read_csv(FILE_NAME)

        rank = df.sort_values(
            by="Percentage",
            ascending=False
        )

        rank["Rank"] = range(1, len(rank)+1)

        print("\n========== STUDENT RANKING ==========\n")

        print(
            rank[
                [
                    "Rank",
                    "ID",
                    "Name",
                    "Percentage",
                    "Grade"
                ]
            ]
        )

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Pass / Fail Report
# ============================================================

def pass_fail_report():

    try:

        df = pd.read_csv(FILE_NAME)

        passed = len(df[df["Grade"] != "Fail"])

        failed = len(df[df["Grade"] == "Fail"])

        print("\n========== PASS / FAIL REPORT ==========\n")

        print("Passed Students :", passed)

        print("Failed Students :", failed)

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Subject Wise Topper
# ============================================================

def subject_toppers():

    try:

        df = pd.read_csv(FILE_NAME)

        subjects = [
            "Math",
            "Physics",
            "Chemistry",
            "English",
            "Computer"
        ]

        print("\n========== SUBJECT TOPPERS ==========\n")

        for subject in subjects:

            index = df[subject].idxmax()

            print(subject)

            print("Name :", df.loc[index, "Name"])

            print("Marks :", df.loc[index, subject])

            print("-" * 40)

    except FileNotFoundError:

        print("Database File Not Found")

# ============================================================
# Graph Menu
# ============================================================

def graph_menu():

    while True:

        print("\n")
        print("=" * 50)
        print("        GRAPH MENU")
        print("=" * 50)

        print("1. Bar Chart")
        print("2. Line Chart")
        print("3. Histogram")
        print("4. Pie Chart")
        print("5. Scatter Plot")
        print("6. Box Plot")
        print("7. Count Plot")
        print("8. Seaborn Box Plot")
        print("9. Violin Plot")
        print("10. Heatmap")
        print("11. Pair Plot")
        print("12. Back to Main Menu")

        choice = input("\nEnter Choice : ")

        if choice == "1":
            bar_chart()

        elif choice == "2":
            line_chart()

        elif choice == "3":
            histogram()

        elif choice == "4":
            pie_chart()

        elif choice == "5":
            scatter_chart()

        elif choice == "6":
            box_chart()

        elif choice == "7":
            count_plot()

        elif choice == "8":
            seaborn_boxplot()

        elif choice == "9":
            violin_plot()

        elif choice == "10":
            heatmap_chart()

        elif choice == "11":
            pair_plot()

        elif choice == "12":
            break

        else:
            print("Invalid Choice")


# ============================================================
# Main Menu
# ============================================================

def menu():

    create_database()

    while True:

        print("\n")
        print("=" * 70)
        print(" STUDENT PERFORMANCE MANAGEMENT SYSTEM ")
        print("=" * 70)

        print("1. Add Student")
        print("2. Display Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. View Result")
        print("7. Statistics")
        print("8. Subject Analysis")
        print("9. Topper")
        print("10. Lowest Scorer")
        print("11. Grade Report")
        print("12. NumPy Analysis")
        print("13. Random Student Generator")
        print("14. Student Ranking")
        print("15. Pass / Fail Report")
        print("16. Subject Toppers")
        print("17. Export Top Students")
        print("18. Backup Database")
        print("19. Graph Menu")
        print("20. Exit")

        choice = input("\nEnter Choice : ")

        if choice == "1":
            add_student()

        elif choice == "2":
            display_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            view_result()

        elif choice == "7":
            statistics()

        elif choice == "8":
            subject_analysis()

        elif choice == "9":
            topper()

        elif choice == "10":
            lowest_student()

        elif choice == "11":
            grade_report()

        elif choice == "12":
            numpy_analysis()

        elif choice == "13":
            random_students()

        elif choice == "14":
            ranking()

        elif choice == "15":
            pass_fail_report()

        elif choice == "16":
            subject_toppers()

        elif choice == "17":
            export_top_students()

        elif choice == "18":
            backup_database()

        elif choice == "19":
            graph_menu()

        elif choice == "20":
            print("\nThank You for Using the System.")
            break

        else:
            print("Invalid Choice")

# ============================================================
# Filter Students by Grade
# ============================================================

def filter_by_grade():

    try:

        df = pd.read_csv(FILE_NAME)

        grade = input("Enter Grade (A+, A, B, C, D, Fail): ")

        result = df[df["Grade"] == grade]

        if result.empty:
            print("\nNo Students Found.")

        else:
            print("\nStudents with Grade", grade)
            print(result)

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Filter Students by Gender
# ============================================================

def filter_by_gender():

    try:

        df = pd.read_csv(FILE_NAME)

        gender = input("Enter Gender (Male/Female): ")

        result = df[
            df["Gender"].str.lower() == gender.lower()
        ]

        if result.empty:

            print("\nNo Students Found.")

        else:

            print(result)

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Class Summary
# ============================================================

def class_summary():

    try:

        df = pd.read_csv(FILE_NAME)

        print("\n========== CLASS SUMMARY ==========")

        print("Total Students :", len(df))

        print("Average Percentage :",
              round(df["Percentage"].mean(),2))

        print("Highest Percentage :",
              df["Percentage"].max())

        print("Lowest Percentage :",
              df["Percentage"].min())

        print("\nGrade Distribution")

        print(df["Grade"].value_counts())

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Save Summary Report
# ============================================================

def save_summary():

    try:

        df = pd.read_csv(FILE_NAME)

        with open("summary_report.txt", "w") as file:

            file.write("STUDENT SUMMARY REPORT\n")
            file.write("="*40 + "\n")

            file.write(f"Total Students : {len(df)}\n")
            file.write(
                f"Average Percentage : {round(df['Percentage'].mean(),2)}\n"
            )
            file.write(
                f"Highest Percentage : {df['Percentage'].max()}\n"
            )
            file.write(
                f"Lowest Percentage : {df['Percentage'].min()}\n"
            )

            file.write("\nGrade Distribution\n")
            file.write(str(df["Grade"].value_counts()))

        print("\nSummary Saved Successfully.")

    except FileNotFoundError:

        print("Database File Not Found")


# ============================================================
# Main Program
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("STUDENT PERFORMANCE MANAGEMENT SYSTEM")
    print("=" * 60)

    try:

        menu()

    except KeyboardInterrupt:

        print("\nProgram Interrupted.")

    except Exception as error:

        print("\nUnexpected Error")
        print(error)

    finally:

        print("\nProgram Closed Successfully.")