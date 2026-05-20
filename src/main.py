import re
import json
import os

with open("input/raw-text.txt", "r") as file:
    raw_text = file.read()


patterns = {
    # 1. Generic Email
    "email": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
   
    # 2. ALU Email (Changed to non-capturing group (?:...) and handles potential .org/.edu/.com)
    "alu_email": r"\b[a-zA-Z0-9._%+-]+@(?:alueducation|alumni\.alueducation|si\.alueducation)\.[a-zA-Z]{2,}\b",
   
    # 3. Credit Cards (Simplified to match 13-16 digits that may have spaces/dashes)
    "credit_cards": r"\b(?:\d[\s-]*){13,16}\b",
   
    # 4. URL
    "url_pattern": r"https?://[^\s]+",
   
    # 5. Hashtag 
    "hashtag_pattern": r"#[a-zA-Z0-9_]+"
}


#now we will mask the credit card numbers by relacing all but the last 4 digits with asterisks. We will also remove any spaces or dashes from the credit card number before masking.
def mask_credit_card(card_number): 
    digits_only = re.sub(r'[\s\-]', '', card_number)
    masked = '*' * (len(digits_only) - 4) + digits_only[-4:]
    return masked

# Now we will loop through the patterns, find matches in the raw text, and store the results in a dictionary. For credit card numbers, we will mask them before storing.
results = {}


for label, pattern in patterns.items():
    matches = re.findall(pattern, raw_text)
    if label == "credit_cards":
        matches = [mask_credit_card(match) for match in matches]
   
    results[label] = {
        "matches": matches,
        "count": len(matches),
    }
with open("output/sample_output.json", "w") as output_file:
    json.dump(results, output_file, indent=4)
       
#Now we will print a message to the console indicating that the results have been saved to the output file.
print("Results have been saved to output/sample_output.json")



