from cs50 import get_string

# Prompt user for text
text = get_string("Text: ")

# Count letters
letters = len([let for let in text if let.isalpha()])

# Count Words
words = len(text.split())

# Count sentences
full_stop = text.count(".")
excalmation = text.count("!")
question = text.count("?")
sentences = full_stop + excalmation + question

# Grade text
L = letters / words * 100
S = sentences / words * 100

# Calculate Coleman-Liau index
grade = round(0.0588 * L - 0.296 * S - 15.8)

# Print Grade
if grade < 1:
    print("Before Grade 1")
elif grade > 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")
