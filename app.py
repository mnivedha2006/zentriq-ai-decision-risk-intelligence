import streamlit as st
import os
import json
import pandas as pd

st.set_page_config(
    page_title="Zentriq AI Decision Risk Intelligence",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Zentriq: AI Decision Risk Intelligence Engine")
st.markdown("Automated meeting document ingestion, quantitative risk scoring, and portfolio health monitoring.")

st.sidebar.header("Document Ingestion")
uploaded_file = st.sidebar.file_uploader("Upload Meeting Transcript (.txt)", type=["txt"])
api_key_input = st.sidebar.text_input("Gemini API Key", type="password", value=os.environ.get("GEMINI_API_KEY", ""))

if api_key_input:
    os.environ["GEMINI_API_KEY"] = api_key_input

if st.sidebar.button("Run Risk Intelligence Pipeline"):
    if not api_key_input:
        st.error("Please provide a valid Gemini API Key.")
    else:
        try:
            from src.document_processor import extract_text_from_file
            from src.ai_extractor import extract_decisions_with_ai
            from src.risk_engine import evaluate_all_decisions
            from src.dashboard_aggregator import aggregate_portfolio_risks

            if uploaded_file is not None:
                temp_path = "temp_transcript.txt"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                doc_text = extract_text_from_file(temp_path)
            else:
                sample_path = "data/sample_documents/project_meeting_01.txt"
                if os.path.exists(sample_path):
                    st.info("No file uploaded. Running pipeline on default sample document.")
                    doc_text = extract_text_from_file(sample_path)
                else:
                    st.error("Please upload a meeting transcript file.")
                    st.stop()

            with st.spinner("Analyzing decisions with Gemini AI and calculating risk metrics..."):
                raw_decisions = extract_decisions_with_ai(doc_text)
                evaluated_decisions = evaluate_all_decisions(raw_decisions)
                portfolio_summary = aggregate_portfolio_risks(evaluated_decisions)

            st.success("Pipeline executed successfully!")

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Decisions", portfolio_summary.get("total_decisions", 0))
            col2.metric("Average Risk Score", f"{portfolio_summary.get('average_portfolio_risk_score', 0):.2f}")
            col3.metric("Portfolio Health", portfolio_summary.get("portfolio_health", "Unknown"))

            st.markdown("---")
            st.subheader("Risk Breakdown")
            st.json(portfolio_summary.get("risk_breakdown", {}))

            st.subheader("Department Risk Summary")
            dept_summary = portfolio_summary.get("department_summary", {})
            if dept_summary:
                st.dataframe(pd.DataFrame.from_dict(dept_summary, orient='index'))

            st.subheader("Top Priorities & Action Items")
            for item in portfolio_summary.get("top_priorities", []):
                with st.expander(f"[{item.get('risk_level', 'Medium')}] {item.get('decision', 'Decision')} (Score: {item.get('risk_score', 0)})"):
                    st.write(f"**Status:** {item.get('status')}")
                    st.write(f"**Owner:** {item.get('owner', 'Unassigned')}")
                    st.write(f"**Business Area:** {item.get('business_area')}")
                    st.write(f"**Risk Factors:** {item.get('risk_factors')}")
                    st.write(f"**Recommendation:** {item.get('recommendation')}")

        except Exception as e:
            st.error(f"An error occurred during pipeline execution: {e}")