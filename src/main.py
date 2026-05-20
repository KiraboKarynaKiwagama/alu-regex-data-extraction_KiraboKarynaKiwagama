import re
import json
import os

with open("input/raw-text.txt", "r") as file:
    raw_text = file.read()


patterns = {
    # 1. Generic Email
    "email": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
   
    # 2. ALU Email
    "alu_email": r"\b[a-zA-Z0-9._%+-]+@(?:alueducation|alumni\.alueducation|si\.alueducation)\.[a-zA-Z]{2,}\b",
   
    # 3. Credit Cards
    "credit_cards": r"\b(?:\d[\s-]*){13,16}\b",
   
    # 4. URL
    "url_pattern": r"https?://[^\s]+",
   
    # 5. Hashtag 
    "hashtag_pattern": r"#[a-zA-Z0-9_]+"
}


# SECURITY CHECK FUNCTION this function checks every match before it gets saved.
# If the match contains hostile content it gets rejected.
def is_safe(value):
    hostile_patterns = [
        r'<script',             # XSS - tries to run javascript
        r'</script>',           # XSS closing tag
        r'javascript:',         # dangerous URL protocol
        r'DROP\s+TABLE',        # SQL injection - deletes database tables
        r'OR\s+[\'"]1[\'"]',    # SQL injection - bypasses login
        r'document\.cookie',    # tries to steal session cookies
        r'window\.location',    # tries to redirect the browser
        r'<iframe',             # iframe injection
        r'onerror\s*=',         # HTML event injection
        r'<img[^>]+src\s*=',    # malicious image tag
        r'--$',                 # SQL comment used to cut off queries
    ]
    for hostile in hostile_patterns:
        if re.search(hostile, value, re.IGNORECASE):
            return False
    return True


# MALFORMED INPUT CHECK Catches broken or suspicious formatting before saving.
def is_well_formed(label, value):
    if label in ["email", "alu_email"]:
        # Reject emails with double @ symbol
        if value.count('@') != 1:
            return False
        # Reject emails that are suspiciously long
        if len(value) > 254:
            return False

    if label == "credit_cards":
        digits_only = re.sub(r'[\s\-]', '', value)
        # Reject cards where all digits are the same e.g. 0000000000000000
        if len(set(digits_only)) == 1:
            return False
        # Reject cards that are not between 13 and 16 digits
        if not (13 <= len(digits_only) <= 16):
            return False

    if label == "url_pattern":
        # Reject URLs that don't start with http or https
        if not value.startswith(("http://", "https://")):
            return False

    return True


# Mask credit card numbers before saving
def mask_credit_card(card_number): 
    digits_only = re.sub(r'[\s\-]', '', card_number)
    masked = '*' * (len(digits_only) - 4) + digits_only[-4:]
    return masked

#Now we run the main extraction and validation loop, saving results in a structured format.
Results = {}

for label, pattern in patterns.items():
    matches = re.findall(pattern, raw_text)

    safe_matches = []
    flagged_matches = []

    for match in matches:
        # Run both security checks on every match
        if not is_safe(match):
            flagged_matches.append(match)
        elif not is_well_formed(label, match):
            flagged_matches.append(match)
        else:
            # Only mask and save if it passed both checks
            if label == "credit_cards":
                safe_matches.append(mask_credit_card(match))
            else:
                safe_matches.append(match)

    Results[label] = {
        "matches": safe_matches,
        "count": len(safe_matches),
        "flagged": flagged_matches,       # saved separately for review
        "flagged_count": len(flagged_matches)
    }


with open("output/sample_output.json", "w") as output_file:
    json.dump(Results, output_file, indent=4)
       
print("Results have been saved to output/sample_output.json")



