from pypdf import PdfReader
import re, json
import argparse

# Argument parser setup
parser = argparse.ArgumentParser(description="Extract MCQs from a SAT-style PDF.")
parser.add_argument("input_pdf", help="Path to the input PDF file")
parser.add_argument("output_json", help="Path to the output JSON file")
args = parser.parse_args()





# Patterns to skip entire pages
UNWANTED_PAGE_PATTERNS = [
    r'^\s*$',  # Completely empty
    r'No Test Material On This Page',
    r'Test begins on the next page',
    r'Make time to take the practice test'
]

# Patterns to skip lines (headers/footers)
SKIP_PATTERNS = [
    r'^\s*\d+\s*QUESTIONS',
    r'^\s*DIRECTIONS',
    r'^\s*The questions in this section',
    r'^\s*All questions in this section',
    r'^\s*Unauthorized copying',
    r'^\s*If you finish',
    r'^\s*Continue',
    r'^\s*Page\s*\d+',
    r'^\s*$',
    r'^\.{5,}$',  
]

skip_res = [re.compile(p, re.IGNORECASE) for p in SKIP_PATTERNS]
unwanted_res = [re.compile(p, re.IGNORECASE) for p in UNWANTED_PAGE_PATTERNS]

def clean_text(txt):
    lines = txt.splitlines()
    cleaned_lines = []
    skip_next = False

    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue

        # Handle "Module" separately
        if re.match(r'^\s*Module\s*\d*$', line, re.IGNORECASE):
            # Skip next line if it's just a number
            if i + 1 < len(lines) and re.match(r'^\s*\d+\s*$', lines[i + 1]):
                skip_next = True
            continue

        if any(rx.match(line) for rx in skip_res):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

def is_unwanted_page(text):
    text = text.strip()
    return any(rx.search(text) for rx in unwanted_res)

# Read and clean PDF pages
reader = PdfReader(args.input_pdf)
full = []
for i, page in enumerate(reader.pages, 1):
    txt = page.extract_text() or ""
    cleaned = clean_text(txt)
    if is_unwanted_page(cleaned):
        continue
    full.append(cleaned)

cleaned_text = "\n".join(full)

# Extract questions with multi-line options
def extract_questions(text):
    lines = text.splitlines()
    questions = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if re.match(r'^\d+$', line):  # Found question number
            question_id = line
            i += 1

            found_options = False
            lookahead_index = i
            while lookahead_index < len(lines):
                look_line = lines[lookahead_index].strip()

                # If next question number (N+1 or 1) is found before A) → skip
                if re.match(r'^\d+$', look_line):
                    next_q = int(look_line)
                    if next_q == int(question_id) + 1 or next_q == 1:
                        found_options = False
                        break

                if re.match(r'^[A-Da-d]\)', look_line):
                    found_options = True
                    break

                lookahead_index += 1

            if not found_options:
                continue  # Skip this question because its not MCQ

            # Collect question text 
            question_lines = []
            while i < len(lines) and not re.match(r'^[A-Da-d]\)', lines[i].strip()):
                question_lines.append(lines[i].strip())
                i += 1

            question_text = ' '.join(question_lines).strip()

            # Collect options
            options = []
            current_option = None

            while i < len(lines):
                line = lines[i].strip()

                if re.match(r'^\d+$', line):
                    break  # New question number

                option_match = re.match(r'^([A-Da-d])\)\s*(.*)', line)

                if option_match:
                    if current_option:
                        options.append(current_option)
                    key, text = option_match.groups()
                    current_option = {"key": key.upper(), "text": text.strip()}
                elif current_option:
                    current_option["text"] += " " + line.strip()
                else:
                    break

                i += 1

            if current_option:
                options.append(current_option)

            if question_text and len(options) >= 2:
                questions.append({
                    "question_id": question_id,
                    "question_type": "single_choice",
                    "question_text": question_text,
                    "options": options
                })
        else:
            i += 1

    return questions


# Extract and write to file
questions = extract_questions(cleaned_text)

with open(args.output_json, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(questions)} questions to {args.output_json}")
