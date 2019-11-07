import cs50
import sys
# verifying command line argument use
if len(sys.argv) != 2:
    print("Usage: python roster.py House")
    exit()
# associating database
db = cs50.SQL("sqlite:///students.db")

dorm = sys.argv[1]
# selecting the students from the house and getting the needed info
roster = db.execute("SELECT first, middle, last, birth FROM students WHERE house = '%s' ORDER BY last, first" % dorm)
# printing middle name if present, otherwise ignoring middle name
for row in roster:
    if row["middle"] == None:
        print(f"{row['first']} {row['last']}, born {row['birth']}")
    else:

        print(f"{row['first']} {row['middle']} {row['last']}, born {row['birth']}")