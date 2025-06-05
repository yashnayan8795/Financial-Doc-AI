import streamlit as st
import json
from mock_pega_workflow import route_workflow
from reconcile_data import reconcile
from ner_predict import extract_entities_from_text
import pandas as pd
import os
import torch


# Set page config
st.set_page_config(
    page_title="Financial Doc AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and instructions
st.title("📄 Financial Document AI")
st.markdown("""
A Smart System for Entity Extraction, Validation, and Reconciliation of Financial Docs.

### 📝 Instructions
1. Upload a financial document (PDF or TXT).
2. Choose an action: Entity Extraction & Validation or Reconciliation.
3. View and download the output.
""")

# Sidebar
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a file (PDF or TXT)", type=["pdf", "txt"])
    action = st.radio("Select Action", ["Extract & Validate", "Reconcile with Golden Source"])

# Main Workflow
if uploaded_file:
    st.success(f"✅ Uploaded: {uploaded_file.name}")

    # Read uploaded file content
    file_text = uploaded_file.read().decode("utf-8")

    # Entity Extraction
    with st.spinner("🔍 Extracting entities..."):
        extracted_entities = extract_entities_from_text(file_text)

    st.subheader("🧠 Extracted Entities")
    st.json(extracted_entities)

    with st.expander("📄 View Raw Text"):
        st.text(file_text)

    # Validation
    with st.spinner("🔎 Validating entities..."):
        validation_result = route_workflow(extracted_entities)

    if validation_result.get("status") == "error":
        st.error(f"❌ Error: {validation_result['message']}")
    else:
        st.success("✅ Entities validated successfully.")

    # Reconciliation
    if action == "Reconcile with Golden Source":
        if os.path.exists("data/golden_source/golden_data.json"):
            with open("data/golden_source/golden_data.json") as f:
                golden_data = json.load(f)

            st.info("🔁 Running Reconciliation with golden source...")
            recon_result = reconcile(extracted_entities, golden_data)

            st.subheader("🔍 Reconciliation Result")
            st.dataframe(recon_result)


            csv_data = recon_result.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Reconciliation Report",
                data=csv_data,
                file_name="reconciliation_report.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Golden source file not found at 'data/golden_source/golden_data.json'")

else:
    st.info("⬅️ Please upload a file to begin.")



if not hasattr(torch, 'classes'):
    torch.classes = type('classes', (), {})()