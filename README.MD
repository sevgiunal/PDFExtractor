# 📝 SAT-style PDF MCQ Extractor

This Python script extracts multiple-choice questions (MCQs) from SAT-style practice test PDFs and saves them in a structured JSON format. It's designed to handle the typical layout and formatting of official digital SAT practice PDFs.

---

## 🧠 Overview

Standardized test PDFs (like those from the SAT) often contain non-question content such as instructions, headers, and filler pages. This script performs the following:

- Parses text from each PDF page
- Removes unwanted lines and pages
- Identifies multiple-choice questions with options
- Outputs clean and structured JSON

---

## ⚙️ Usage

### Run the script from terminal:

```bash
python extract_questions.py <input_pdf> <output_json>
```

**Example:**

```bash
python extract_questions.py sat-practice-test-4-digital.pdf extracted_questions.json
```

This command will extract all identifiable multiple-choice questions from the given PDF and save them to `extracted_questions.json`.

---

### 📂 Input Assumptions

This script is built with SAT Digital Practice PDFs in mind and assumes:

- Each question starts with a standalone number (e.g., 17)
- Answer choices are labeled A), B), C), D) (case-insensitive)
- Choices may span multiple lines
- There may be filler text, headers, or directions that should be ignored
- The PDF text is extractable (not a scanned image or image-based PDF)

---

## 🏗️ High-Level Design

### 1. Argument Parsing

The script uses `argparse` to accept:

- `input_pdf`: the path to the PDF file
- `output_json`: the desired output file path

---

### 2. PDF Reading

Uses `pypdf.PdfReader` to extract text from every page:

```python
reader = PdfReader(args.input_pdf)
```

---

### 3. Text Cleaning

#### Skipping Pages

A set of regex patterns filters out entire pages that contain known filler text like:

- `No Test Material On This Page`
- `Make time to take the practice test`
- Empty or whitespace-only pages

#### Skipping Lines

A separate set of patterns removes lines like:

- Headers: `Page 2`, `DIRECTIONS`, etc.
- Footers: `Unauthorized copying`, etc.
- Module metadata like `Module 3` followed by a number

These filters ensure only relevant question/option content is retained.

---

### 4. Question Extraction Logic

The script loops through cleaned lines and:

- Detects a question number (e.g., 23)
- Looks ahead for A), B), etc. to confirm it’s a multiple-choice question
- Collects question text and options (supports multi-line options)
- Builds structured dictionaries like:

```json
{
  "question_id": "23",
  "question_type": "single_choice",
  "question_text": "Which of the following is true based on the passage?",
  "options": [
    {"key": "A", "text": "The author supports the claim..."},
    {"key": "B", "text": "The passage describes..."},
    {"key": "C", "text": "It is implied that..."},
    {"key": "D", "text": "The main idea is..."}
  ]
}
```

---

### 5. Output to JSON

At the end, the full list of extracted questions is dumped to the specified JSON file using:

```python
json.dump(questions, f, indent=2, ensure_ascii=False)
```

---

## 📦 File Structure

```bash
.
├── extract_questions.py              # Main script
├── sat-practice-test-4-digital.pdf  # Input PDF (example)
├── extracted_questions.json         # Output (example)
└── README.md                        # This file
```

---

## ✅ Output Example

```json
[
  {
    "question_id": "1",
    "question_type": "single_choice",
    "question_text": "What is the value of x in the equation above?",
    "options": [
      {"key": "A", "text": "2"},
      {"key": "B", "text": "4"},
      {"key": "C", "text": "6"},
      {"key": "D", "text": "8"}
    ]
  },
  ...
]
```

---

## 🧪 Dependencies

- Python 3.7+
- `pypdf`

Install with:

```bash
pip install pypdf
```

---

## 🧱 Regex Filters

### Page Skip Patterns

```python
UNWANTED_PAGE_PATTERNS = [
    r'^\s*$',
    r'No Test Material On This Page',
    r'Test begins on the next page',
    r'Make time to take the practice test'
]
```

### Line Skip Patterns

```python
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
    r'^\.{5,}$'
]
```

---

## 📌 Assumptions

- Only multiple-choice questions are extracted
- Non-MCQs like grid-ins or short answers are ignored
- All options start with A), B), etc.
- The format follows typical SAT Digital layout

---

## 🛠️ Future Improvements

- Add OCR support for scanned/image-based PDFs
- Extract short-answer or numeric-entry questions
- Auto-detect answer keys (if embedded)
- CLI flags for debug/verbose mode or filtering by module
