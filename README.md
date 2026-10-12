# 🧬 FamilySearch Record Linker & Duplicate Finder

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Build Status](https://img.shields.io/badge/tests-3%20passed-brightgreen.svg)
![Code Style](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

An open-source, resilient Python service designed to automate data standardization, fuzzy identity matching, and duplicate profile detection for historical census and genealogical datasets. Built in alignment with the record linking methodologies of **FamilySearch** and the **BYU Record Linking Lab (RLL)**.

---

## 👤 Developer Profile

- **Developer:** Javiera Allende  (*Javiam Allen*)
- **GitHub:** [@javiamallen](https://github.com/javiamallen)
- **Program:** Bachelor of Science in Software Development | **BYU-Pathway Worldwide**
- **Course:** CSE 111: Programming with Functions 2026

---

## 🎯 Problem Statement & Impact

### The Problem
Genealogical platforms like FamilySearch and research environments like the BYU Record Linking Lab process millions of historical census records containing transcript errors, optical character recognition (OCR) flaws, spelling variations, and phonetic misspellings (e.g., *"John Smith"* vs. *"Jon Smith"*). Manual duplication resolution across massive datasets is inefficient and prone to human oversight.

### The Solution
This tool provides an automated pipeline that ingests census records, normalizes unstructured text using Regular Expressions (RegEx), and applies a **Bigram-based Jaccard Similarity Algorithm** combined with birth-year tolerance filters to accurately link candidate profiles and flag duplicate entries.

### Key Metrics & Architectural Impact
- **Zero-Downtime Ingestion:** Integrates HTTP live endpoint fetching with an automated local JSON fallback mechanism, guaranteeing continuous execution even during network API outages.
- **Accuracy & Sensitivity:** Configured with token-overlap bigrams to achieve reliable matching on common typographical errors (identifying duplicates with confidence scores ranging from 70% to 93%+).
- **Quality Assurance:** 100% test coverage using `pytest`, following strict PEP 8 coding standards and pure function practices.

---

## 🛠️ Key Technical Features

1. **Fault-Tolerant Data Ingestion (`requests` + JSON Fallback):** Attempts live HTTP fetching from remote census CSV/JSON repositories. Automatically redirects to `fallback_data.json` upon network failure or 404 responses.
2. **Text Normalization (`re` module):** Strips punctuation, non-alphabetic characters, and redundant whitespace while converting text to uniform uppercase representation.
3. **Fuzzy String Matching Algorithm:** Evaluates character bigram intersections and unions to compute positional similarity ratios between candidate names.
4. **Demographic Constraint Validation:** Validates birth-year deltas ($\le 1$ year tolerance) alongside similarity scores to prevent false positive matches.

---

## 📂 Project Structure

```text
familysearch-record-linker/
│
├── familysearch_matcher.py        # Core application logic & data pipeline
├── test_familysearch_matcher.py   # Automated unit testing suite (pytest)
├── fallback_data.json             # Local backup dataset for offline resilience
├── project_report.txt             # Academic report and Table of Work
├── proposal.txt                   # Initial project architectural design
└── README.md                      # Project documentation and technical brochure