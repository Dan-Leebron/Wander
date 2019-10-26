import csv
import sys

#making sure we have the right amount of command line arguments
if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit()

#opening the CSV into a dictreader, loading the dna sequence into a string that we can read in seq
database = csv.DictReader(open(sys.argv[1], "r"))
strand = open(sys.argv[2], "r")
seq = strand.read()

#giving ourselves an object (rows) that we can use to go over the rows of the dictreader
#num gives how long the actual dna strand is, we need this to iterate over to find repeats
rows = list(database)
num = len(seq)


#getting the sequences we are looking for repeats for
fields = database.fieldnames
fieldnum = len(fields)

#making an empty list which we will use to store the max number of repeats
maxes = list()
#for each sequence we are examining the dna strand at each location and seeing if there is a repeat starting from that position
#if there is a repeat then we move to the next sequence section of the appropriate size and see if that is a repeat too
#there is a temp variable for each location storing the max, if this is larger than the overall max we update the overall max and at the end save the overall max
for j in range(fieldnum - 1):
    maxrepeat = 0
    for i in range(num):
        temp = 0
        k = i
        while seq[k:k + len(fields[j + 1])] == fields[j + 1]:
            temp += 1
            if temp >= maxrepeat:
                maxrepeat = temp
            k += len(fields[j + 1])
    maxes.append(maxrepeat)

#checking all the names in the csv file. If the max number of repeats for the name is equal to the max repeats we saw for the sequence, increase a counter
#if the counter equals the number of field names minus one (because of the name) then all of the maxes match and we print the person
#otherwise if they do not all match print no match
for row in rows:
    counter = 0
    for fieldname in range(fieldnum - 1):
        if maxes[fieldname] == int(row[fields[fieldname + 1]]):
            counter += 1
            if counter == fieldnum - 1:
                print(row['name'])
                exit()
print("No Match")