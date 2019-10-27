from cs50 import get_string

# getting the sentnece
text = get_string("Text: ")
# the counters for letters, words and sentences
let = 0
words = 1
sent = 0

# adding to the counters when we have letters, spaces designating words or punctuation for sentences
for i in text:
    if i.isalpha():
        let += 1
    if i == " ":
        words += 1
    if i == "!" or i == "." or i == "?":
        sent += 1

# the equations
L = 100 * (let / words)
S = 100 * (sent / words)
index = round(0.0588 * L - 0.296 * S - 15.8)

# making sure we only print the grade for cases which make sense
if index > 16:
    print("Grade 16+")
elif index < 1:
    print("Before Grade 1")
else:
    print(f"Grade {index}")