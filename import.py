import csv
import sys
import cs50


# making sure we have the right amount of command line arguments
if len(sys.argv) != 2:
    print("Usage: python import.py characters.csv")
    exit()
# associating the database
db = cs50.SQL("sqlite:///students.db")

with open(sys.argv[1], "r") as titles:

    reader = csv.DictReader(titles)

    for row in reader:
        nameparts = row["name"].split()
# if there is a middle name, including it, or if not then making it null
        if len(nameparts) == 3:
            first = nameparts[0]
            mid = nameparts[1]
            last = nameparts[2]
        else:
            first = nameparts[0]
            mid = None
            last = nameparts[1]
# putting everything into the database
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                   first, mid, last, row["house"], row["birth"])

