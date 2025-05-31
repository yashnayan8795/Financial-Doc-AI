import streamlit as st
import os
import json

from mock_pega_workflow import route_workflow
from reconcile_data import reconcile
from audit import write_audit_log
from data.ner_training.ner_predict import extract_entities_from_text


st.set_page_config(page_title="Financial Doc AI", layout="wide")
st.title("📄 AI-Powered Financial Document Automation")

uploaded_file = st.file_uploader("Upload financial document", type=["txt"])
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    st.subheader("📌 Raw Text")
    st.text(text)

    # 1) Run NER to get a dict { label: entity_text }
    entities = extract_entities_from_text(text)
    st.subheader("🔍 Extracted Entities")
    st.json(entities)

    # 2) Run PEGA validation/routing
    pega_result = route_workflow(entities)
    st.subheader("✅ PEGA Workflow Result")
    st.json(pega_result)

    # 3) Load the golden (ground-truth) data from JSON
    golden_path = "data/golden_source/golden_source.json"
    if os.path.exists(golden_path):
        with open(golden_path) as f:
            golden_dict = json.load(f)
    else:
        st.error(f"Golden source file not found at {golden_path}")
        st.stop()  # stop the app here if golden is missing

    # 4) Run reconciliation: pass both extracted and golden
    recon_result = reconcile(entities, golden_dict)
    st.subheader("📊 Reconciliation Result")
    st.json(recon_result)

    # 5) Write to audit log
    write_audit_log({
        "extracted": entities,
        "pega_result": pega_result,
        "reconciliation": recon_result
    })
    st.success("✅ Audit log updated.")

    # 6) Show the latest audit log
    audit_path = "data/audit_logs/audit_result.json"
    if os.path.exists(audit_path):
        with open(audit_path) as f:
            logs = json.load(f)
        st.subheader("🗂️ Audit Trail")
        st.json(logs)
