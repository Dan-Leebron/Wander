import cs50
import sys

if len(sys.argv) != 2:
    print("Usage: python roster.py House")
    exit()

db = cs50.SQL("sqlite:///students.db")

dorm = sys.argv[1]

roster = db.execute("SELECT first, middle, last, birth FROM students WHERE house = '%s' ORDER BY last, first" % dorm)

for row in roster:
    if row["middle"] == None:
        print(f"{row['first']} {row['last']}, born {row['birth']}")
    else:

        print(f"{row['first']} {row['middle']} {row['last']}, born {row['birth']}")