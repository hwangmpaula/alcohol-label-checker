# AI-Powered Alcohol Label Verification App

## Project Summary

This project is a prototype AI-powered alcohol label verification app. It allows a user to upload an alcohol label image and receive a first-pass compliance review.

The app uses AI vision to extract visible label information, then reviews the extracted information for possible compliance concerns such as missing required fields, unclear label details, risky claims, or items that should be escalated to a human reviewer.

This tool does **not** legally approve alcohol labels. It is designed to support human compliance reviewers by identifying possible issues and organizing the review results in a clear format.

---

## Purpose

Alcohol label compliance review can involve checking many required details, including product identity, alcohol percentage, net contents, health warnings, producer/importer information, and marketing claims.

This prototype helps reduce manual review effort by:

* Extracting visible information from uploaded label images
* Identifying required fields that are not visible in the uploaded image
* Flagging possible compliance risks
* Producing a plain-English summary for human review
* Separating AI-assisted screening from final human decision-making

---

## App Workflow

1. The user uploads an alcohol label image.
2. Layer 1 extracts visible label information from the image.
3. Layer 2 performs a second-level compliance review.
4. Layer 3 generates a final reviewer-friendly report.
5. A human compliance reviewer makes the final decision.

---

## System Layers

### Layer 1: Label Information Extraction

Layer 1 uses AI vision to extract visible information from the uploaded image.

It attempts to identify:

* Brand name
* Product type or alcohol category
* Alcohol percentage / ABV
* Net contents
* Government health warning
* Producer, bottler, importer, or distributor information
* Country or place of origin
* Marketing claims
* Full visible label text

If information is not visible in the uploaded image, the app does not assume it is absent from the full product label. Instead, it marks the information as not visible.

---

### Layer 2: Compliance Review

Layer 2 reviews the extracted label information and checks for possible compliance concerns.

It looks for:

* Required information that is not visible
* Missing or unclear ABV/alcohol percentage
* Missing or unclear net contents
* Missing or unclear government health warning
* Missing or unclear producer/importer information
* Conflicting product names, locations, or descriptions
* Risky health, medical, energy, cure, or performance claims
* Child-appealing language or design concerns
* General readability and clarity issues

Layer 2 does not make a legal approval decision. It flags items that may require human review.

---

### Layer 3: Final Report Generator

Layer 3 organizes the results into a reviewer-friendly report.

The report includes:

* Status: Pass / Needs Review / Fail
* Risk level: Low / Medium / High
* Compliance score
* Main finding
* Key label information
* Issues flagged
* Recommended next step
* Human-review disclaimer

---

## Example Output

For a front-label-only image, the app may return:

* **Status:** Needs Review
* **Risk Level:** Medium
* **Main Finding:** The uploaded image shows the brand name and product type, but ABV, net contents, health warning, and producer/importer details are not visible.
* **Recommended Action:** Upload the back label, side label, neck label, packaging, or full container view for complete review.

This behavior is intentional. The app distinguishes between information that is truly problematic and information that is simply not visible in the uploaded image.

---

## Technology Used

* Python
* Streamlit
* Gemini API
* Google GenAI Python SDK
* Pillow
* python-dotenv

---

## How to Run the App Locally

### 1. Clone or download the project folder

Open the project folder in Visual Studio Code.

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

On Mac:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Create a `.env` file

Create a file named `.env` in the main project folder.

Add your Gemini API key:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not use quotation marks. Do not upload this file to GitHub.

### 6. Run the app

```bash
python -m streamlit run app.py
```

Then open the local Streamlit URL in your browser.

---

## Project Files

```text
alcohol-label-checker/
│
├── app.py
├── checker.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

The `.env` file should remain local and should not be committed to GitHub.

---

## Requirements

The `requirements.txt` file should include:

```text
streamlit
python-dotenv
pillow
google-genai
```

---

## Limitations

This is a prototype and has several limitations:

* It depends on the quality of the uploaded image.
* It may not detect text that is blurry, hidden, cropped, or too small.
* It may require multiple views of the product label for a complete review.
* It does not replace a qualified human compliance reviewer.
* It does not provide legal approval.
* Free-tier AI API limits may apply.

---

## Important Disclaimer

This tool is for prototype and demonstration purposes only. It does not provide legal approval, regulatory certification, or final compliance decisions. All flagged results should be reviewed by a qualified human compliance reviewer before any label is approved or rejected.
