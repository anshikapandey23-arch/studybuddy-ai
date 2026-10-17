StudyBuddy AI starter datasets

Files:
1. engineering_question_bank.csv
   A small starter question bank for demonstrating subject/topic filtering and question search.
   It contains curated example questions and answers; it is not an official AKTU PYQ archive.

2. student_performance_demo.csv
   Synthetic demonstration records for testing charts, weak-topic analysis, and progress views.
   These are not real student records and must be labelled as demo data in presentations.

How to use:
- Place both CSV files in a folder named data inside the StudyBuddy project.
- Install pandas if it is not already installed: pip install pandas
- Load with pd.read_csv("data/engineering_question_bank.csv") and
  pd.read_csv("data/student_performance_demo.csv").

Before real deployment:
- Replace synthetic performance rows with real records only when you have authorization.
- Remove names and direct identifiers, limit access, and follow your institution's privacy rules.
- Verify syllabus and previous-year questions against official AKTU materials before describing them as official.
