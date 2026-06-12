import json
import io
from PIL import Image
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()


def layer_1_extract_label_info(image_file):
    """
    Layer 1: Extract information from the alcohol label image using Gemini vision.
    """

    image_bytes = image_file.getvalue()
    image = Image.open(io.BytesIO(image_bytes))

    prompt = """
You are reviewing an alcohol product label image.

Extract the visible label information and return ONLY valid JSON.

Use this exact JSON structure:

{
  "brand_name": "",
  "product_type": "",
  "alcohol_percentage": "",
  "net_contents": "",
  "government_warning": "",
  "producer_name": "",
  "origin": "",
  "marketing_claims": [],
  "full_label_text": ""
}

Rules:
- If a field is not visible, use an empty string.
- Do not guess.
- Do not write explanation outside the JSON.
- For product_type, identify what it appears to be, such as beer, whiskey, wine, soju, vodka, etc.
- For marketing_claims, list any promotional or health-related claims visible on the label.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, image]
    )

    text_output = response.text.strip()
    text_output = text_output.replace("```json", "").replace("```", "").strip()

    extracted_data = json.loads(text_output)

    return extracted_data


def layer_2_check_compliance(label_data, image_file):
    """
    Layer 2: AI compliance review using the extracted label data and uploaded image.
    This does not give legal approval. It flags possible risks for human review.
    """

    image_bytes = image_file.getvalue()
    image = Image.open(io.BytesIO(image_bytes))

    prompt = f"""
You are an AI alcohol label compliance review assistant.

Your job is to perform a second-level review of alcohol label information after the basic checklist has been completed.

You are not giving legal approval. Your role is to identify possible compliance risks, inconsistencies, missing details, unclear wording, and items that should be reviewed by a human compliance specialist.

Here is the extracted label data from Layer 1:

{json.dumps(label_data, indent=2)}

Review the alcohol label for:

1. Required information
   - Brand name
   - Alcohol type/category
   - ABV or alcohol percentage
   - Net contents
   - Government health warning
   - Producer, bottler, importer, or distributor information
   - Country or place of origin

2. Consistency issues
   - Does the alcohol type match the product description?
   - Does the ABV appear reasonable for the stated alcohol type?
   - Are bottle size and measurement units clear?
   - Are producer/importer details complete enough?
   - Does the label use conflicting names, locations, or product descriptions?

3. Readability and clarity
   - Is important information hard to read?
   - Is the label blurry, crowded, hidden, too small, or confusing?
   - Are required statements easy to identify?

4. Risk flags
   - Missing health warning
   - Missing ABV
   - Missing net contents
   - Unclear alcohol category
   - Misleading product claims
   - Child-appealing language or design
   - Health, energy, cure, medical, or performance claims
   - Conflicting origin or producer information

Return ONLY valid JSON using this exact structure:

{{
  "status": "Pass / Needs Review / Fail",
  "risk_level": "Low / Medium / High",
  "compliance_score": 0,
  "basic_required_information": {{
    "brand_name": {{
      "status": "Found / Missing / Unclear",
      "evidence": ""
    }},
    "alcohol_type": {{
      "status": "Found / Missing / Unclear",
      "evidence": ""
    }},
    "alcohol_percentage": {{
      "status": "Found / Missing / Unclear",
      "evidence": ""
    }},
    "net_contents": {{
      "status": "Found / Missing / Unclear",
      "evidence": ""
    }},
    "health_warning": {{
      "status": "Found / Missing / Unclear",
      "evidence": ""
    }},
    "producer_importer_information": {{
      "status": "Found / Missing / Unclear",
      "evidence": ""
    }},
    "country_or_origin": {{
      "status": "Found / Missing / Unclear",
      "evidence": ""
    }}
  }},
  "consistency_review": {{
    "product_category_consistency": "",
    "abv_consistency": "",
    "size_unit_consistency": "",
    "producer_importer_consistency": "",
    "origin_consistency": ""
  }},
  "readability_review": {{
    "rating": "Clear / Somewhat clear / Unclear",
    "notes": ""
  }},
  "possible_issues": [],
  "issues": [],
  "human_review_needed": "Yes / No",
  "reason_for_human_review": "",
  "plain_english_summary": "",
  "recommended_action": ""
}}

Important rules:
- Do not claim the product is legally approved.
- Do not claim the full label package is noncompliant unless the uploaded image clearly proves a compliance problem.
- If required information is not visible in the uploaded image, say "not visible in uploaded image" instead of "missing."
- If the uploaded image appears incomplete or only shows the front label, use "Needs Review" and recommend uploading the back label, side label, neck label, packaging, or full container view.
- Use "Fail" only when the image clearly shows a prohibited, misleading, conflicting, or high-risk compliance issue.
- Be conservative, reviewer-friendly, and clear.
- Return JSON only. No markdown. No extra explanation.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, image]
    )

    text_output = response.text.strip()
    text_output = text_output.replace("```json", "").replace("```", "").strip()

    compliance_result = json.loads(text_output)

    return compliance_result


def layer_3_generate_report(extracted_data, compliance_result):
    """
    Layer 3: Generate a final plain-English report.
    """

    issues = compliance_result.get("issues", [])

    if not issues:
        issue_summary = "No major issues were detected by the automated review."
    else:
        issue_summary = "The automated review found one or more issues that should be checked."

    final_report = {
        "summary": {
            "brand_name": extracted_data.get("brand_name"),
            "product_type": extracted_data.get("product_type"),
            "alcohol_percentage": extracted_data.get("alcohol_percentage"),
            "net_contents": extracted_data.get("net_contents")
        },
        "result": {
            "status": compliance_result.get("status"),
            "risk_level": compliance_result.get("risk_level"),
            "compliance_score": compliance_result.get("compliance_score"),
            "issue_summary": issue_summary,
            "recommended_action": compliance_result.get("recommended_action")
        },
        "issues": issues,
        "disclaimer": "This prototype does not legally approve alcohol labels. A human compliance reviewer should make the final decision."
    }

    return final_report


def run_full_check(image_file):
    """
    Runs the full alcohol label checker process:
    Layer 1 → Layer 2 → Layer 3
    """

    extracted_data = layer_1_extract_label_info(image_file)
    compliance_result = layer_2_check_compliance(extracted_data, image_file)
    final_report = layer_3_generate_report(extracted_data, compliance_result)

    return extracted_data, compliance_result, final_report