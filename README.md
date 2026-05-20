# ALU Regex Data Extraction

## What This Project Does
This program scans a raw server log text file and automatically extracts 
specific types of structured data using regex (regular expression) patterns. 
It also detects and flags malicious or malformed input before saving clean 
results to a JSON output file.

---

## How to Run It

### Requirements
- Python 3.x installed on your machine

### Steps
1. Clone or download this repository
2. Open your terminal and navigate to the project root folder:
3. Run the main script:
4. Check the results in:

   Project Structure
   alu-regex-data-extraction-KiraboKarynaKiwagama/
├── input/
│   └── raw-text.txt        # The raw messy text that gets scanned
├── src/
│   └── main.py             # All regex patterns and program logic
├── output/
│   └── results.json        # The extracted results saved here
└── README.md               # This file

---

## Data Types Extracted

| Type | Pattern Used | Notes |
|---|---|---|
| Emails | `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` | Catches all valid emails |
| ALU Emails | `[a-zA-Z0-9._%+-]+@(alueducation\|alumni\.alueducation\|si\.alueducation)\.com` | Only official ALU addresses |
| Credit Cards | `\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b` | Masked before saving |
| URLs | `https?:\/\/[^\s]+` | Must start with http or https |
| Hashtags | `#[a-zA-Z]\w+` | Must start with a letter after # |

---

## ALU Email Validation
The program specifically validates three official ALU email formats:
- `@alueducation.com` — main staff and student emails
- `@alumni.alueducation.com` — alumni network emails
- `@si.alueducation.com` — social innovation department emails

Any address not matching these exact domains is treated as a general 
external email and stored separately.

---

## Security Considerations

The program does not automatically trust the input file. Every match is 
checked against a list of known hostile patterns before being saved.

### What Gets Flagged and Rejected
| Threat | Example | Why It's Dangerous |
|---|---|---|
| XSS injection | `<script>document.cookie</script>` | Steals user session data |
| SQL injection | `'; DROP TABLE users;--` | Destroys database records |
| JavaScript URLs | `javascript:void(0)` | Executes code in the browser |
| iframe injection | `<iframe src="http://evil.com">` | Loads malicious pages |
| Malformed emails | `user@@domain.com` | Sign of spoofing attempt |

### How Sensitive Data is Handled
- Credit card numbers are **never saved in full**
- All digits except the last 4 are replaced with `*` before writing to output
- Example: `4111-2222-3333-4464` becomes `************4464`
- Flagged matches are recorded separately so they can be reviewed

---

## Sample Output
```json
{
    "emails": {
        "matches": ["j.okafor@healthmail.org", "david@techbridge.com"],
        "count": 2
    },
    "alu_emails": {
        "matches": ["tech-support@si.alueducation.com"],
        "count": 1
    },
    "credit_cards": {
        "matches": ["************4464", "************5100"],
        "count": 2
    },
    "urls": {
        "matches": ["https://api.alueducation.com/v2/auth"],
        "count": 1
    },
    "hashtags": {
        "matches": ["#ALUInnovate2026", "#PanAfricanTech"],
        "count": 2
    }
}
```

---

## Author
- **Name:** Kirabo Karyna Kiwagama
- **GitHub:** KiraboKarynaKiwagama
- **Program:** ALU Software Engineering
