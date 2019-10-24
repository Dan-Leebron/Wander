from cs50 import get_string

text = get_string("Text: ")

let = 0
words = 1
sent = 0

for i in text:
    if i.isalpha():
        let += 1
    if i == " ":
        words += 1
    if i == "!" or i == "." or i == "?":
        sent += 1

L = 100 * (let / words)
S = 100 * (sent / words)
index = round(0.0588 * L - 0.296 * S - 15.8)


if index > 16:
    print("Grade 16+")
elif index < 1:
    print("Before Grade 1")
else:
    print(f"Grade {index}")