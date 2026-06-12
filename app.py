import streamlit as st
from checker import run_full_check

st.set_page_config(
    page_title="AI Alcohol Label Verification App",
    page_icon="🍺",
    layout="centered"
)

st.title("AI Alcohol Label Verification App")
st.caption("Prototype tool for first-pass alcohol label screening and human review support.")

st.markdown(
    """
    Upload an alcohol label image. The app will extract visible label information,
    check for possible compliance risks, and generate a reviewer-friendly summary.

    **Important:** This tool does not legally approve alcohol labels. It only flags items for human review.
    """
)

uploaded_file = st.file_uploader(
    "Upload alcohol label image",
    type=["jpg", "jpeg", "png"]
)


def clean_issue_wording(issue):
    issue = str(issue)

    replacements = {
        "Missing mandatory alcohol percentage.": "Alcohol percentage not visible in uploaded image.",
        "Missing mandatory net contents.": "Net contents not visible in uploaded image.",
        "Missing mandatory government health warning.": "Government health warning not visible in uploaded image.",
        "Missing mandatory producer/importer/distributor information.": "Producer, importer, or distributor information not visible in uploaded image.",
        "Missing Alcohol By Volume (ABV) statement.": "Alcohol By Volume (ABV) statement not visible in uploaded image.",
        "Missing Government Health Warning statement.": "Government health warning statement not visible in uploaded image.",
        "Missing ABV": "ABV not visible in uploaded image.",
        "Missing net contents": "Net contents not visible in uploaded image.",
        "Missing government health warning": "Government health warning not visible in uploaded image.",
        "Missing producer/importer details": "Producer/importer details not visible in uploaded image."
    }

    return replacements.get(issue, issue)


if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Label Image", use_container_width=True)

    if st.button("Run Label Review", type="primary"):
        with st.spinner("Reviewing label..."):
            try:
                extracted_data, compliance_result, final_report = run_full_check(uploaded_file)

                st.session_state["extracted_data"] = extracted_data
                st.session_state["compliance_result"] = compliance_result
                st.session_state["final_report"] = final_report

            except Exception as e:
                st.error("The label review could not be completed.")
                st.write("Check your API key, internet connection, package installation, or uploaded image.")
                with st.expander("Technical error details"):
                    st.exception(e)


if "final_report" in st.session_state:
    extracted_data = st.session_state["extracted_data"]
    compliance_result = st.session_state["compliance_result"]
    final_report = st.session_state["final_report"]

    result = final_report.get("result", {})
    summary = final_report.get("summary", {})

    issues = final_report.get("issues", [])

    if not issues:
        issues = compliance_result.get("issues", [])

    if not issues:
        issues = compliance_result.get("possible_issues", [])

    status = result.get("status", compliance_result.get("status", "Needs Review"))
    risk_level = result.get("risk_level", compliance_result.get("risk_level", "Unknown"))
    score = result.get("compliance_score", compliance_result.get("compliance_score", "N/A"))
    recommended_action = result.get(
        "recommended_action",
        compliance_result.get("recommended_action", "Send to human reviewer.")
    )

    st.divider()

    st.subheader("Final Review Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Status", status)
    col2.metric("Risk Level", risk_level)
    col3.metric("Score", score)

    if status == "Pass":
        st.success("The uploaded label image appears acceptable based on the automated review.")
    elif status == "Needs Review":
        st.warning("The uploaded label image needs human review before approval.")
    else:
        st.error("The uploaded label image has serious issues that should be reviewed or corrected.")

    st.markdown("### Main Finding")

    plain_summary = compliance_result.get(
        "plain_english_summary",
        result.get("issue_summary", "The review found items that should be checked.")
    )

    st.write(plain_summary)

    st.markdown("### Recommended Next Step")
    st.info(recommended_action)

    st.markdown("### Key Label Information")

    label_col1, label_col2 = st.columns(2)

    with label_col1:
        st.write("**Brand Name:**", summary.get("brand_name") or "Not visible")
        st.write("**Product Type:**", summary.get("product_type") or "Not visible")

    with label_col2:
        st.write("**Alcohol Percentage:**", summary.get("alcohol_percentage") or "Not visible")
        st.write("**Net Contents:**", summary.get("net_contents") or "Not visible")

    st.markdown("### Issues Flagged")

    if issues:
        for issue in issues:
            st.write(f"- {clean_issue_wording(issue)}")
    else:
        st.write("No major issues were flagged by the automated review.")

    st.divider()

    st.subheader("Detailed Review")

    with st.expander("Layer 1: Extracted Label Information"):
        st.json(extracted_data)

    with st.expander("Layer 2: Compliance Review"):
        st.json(compliance_result)

    with st.expander("Layer 3: Final Report"):
        st.json(final_report)

    st.divider()

    st.caption(
        "Disclaimer: This prototype does not legally approve alcohol labels. "
        "A human compliance reviewer should make the final decision."
    )

else:
    st.info("Upload a label image and click 'Run Label Review' to begin.")