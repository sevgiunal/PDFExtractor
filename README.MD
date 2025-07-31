# PDF Question Extractor

This project automates the extraction of structured question-answer data from educational PDFs. It is particularly tailored for quiz-style documents with both text and image-based questions, like the BBC Skillswise quiz PDF used here.

---

## Objective

The goal is to extract **questions**, **options**, **images (if any)**, and **answers with explanations** from a quiz-style PDF and store the results in a structured JSON format (`questions.json`).

---

## High-Level Approach

### 1. **Download & Prepare PDF**
- A PDF is downloaded from a given URL and saved locally.
- The directory structure is created to store extracted assets like:
  - Raw text
  - Images from pages
  - Extracted tables
  - Rendered full-page images

---

### 2. **Parse PDF Page-by-Page**
Using `PyMuPDF` and `tabula-py`:
- **Text content** is extracted and saved per page.
- **Tables** are detected and stored.
- **Images** on the page (inline figures, charts, etc.) are extracted.
- **Page-level screenshots** are saved for full visual context.

---

### 3. **Identify & Extract Questions**
- Text is parsed using regex to identify quiz questions.
- Supports both:
  - **Text-based MCQs** (A) Option 1, (B) Option 2…
  - **Image-based questions** with associated graphs (e.g., "Which graph best fits...")
- Uses heuristics to determine if a question is graph/image-based based on keywords and lack of text options.

---

### 4. **Parse Answers & Match to Questions**
- The answer section is identified using "Answers" as a split marker.
- Answers are parsed using regex to extract:
  - The original question
  - Correct answer key (e.g., A)
  - Explanation
- Uses **fuzzy matching** to link answer explanations back to their corresponding extracted question.

---

### 5. **Output Structured Data**
- Final structured data is saved as `questions.json` in the format:

```json
{
  "question_id": "3_1",
  "question_type": "single_choice",
  "question_text": "Which graph best represents this situation?",
  "image": ["data/images/BBCPaper_image_3_0_15.png"],
  "options": [
    {"key": "A", "image": "data/images/BBCPaper_image_3_0_15.png"},
    ...
  ],
  "correct_answer": "B",
  "answer_explanation": "Because this graph shows a constant increase over time."
}
## Assumptions Made

### PDF Structure is Consistent:
- Each question starts with a number like `1.`, `2.`, etc.
- Answers follow a consistent pattern with the phrase: `"The correct answer is: A"`.

### Graph-Based Questions Have Multiple Images:
- Detected using keywords like **"graph that best fits..."** and absence of text-based options.

### One Question Block Per Match:
- Each regex match corresponds to one full question (text + options).

### Images and Answers Are On the Same Page as Questions:
- This is assumed for graph-based questions to link image options correctly.

### Answer Key is a Single Letter (A/B/C/D):
- Assumes no multi-select or non-MCQs.

---

## 📁 Output Files

| File                         | Description                                                              |
|------------------------------|--------------------------------------------------------------------------|
| `data/processed_output.json` | Intermediate output containing text, tables, and image metadata by page. |
| `data/questions.json`        | Final extracted questions and answers in a clean structured format.      |
| `data/images/`, `data/text/`, etc. | Assets extracted from the PDF.                                     |

---

## 🛠 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
