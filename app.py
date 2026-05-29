import streamlit as st

# import google.api_core.exceptions as exceptions
from utils import extract_text_from_pdf, get_ats_analysis
# UI Configuration
st.set_page_config(page_title="ResumePro AI", page_icon="📝", layout="wide")

# Updated CSS in app.py
st.markdown(
    """
    <style>
    /* Metric Cards that adapt to Dark/Light mode */
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }

    /* Force text inside metrics to follow the theme's text color */
    div[data-testid="stMetric"] label,
    div[data-testid="stMetricValue"] {
        color: var(--text-color) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🚀 ResumePro: AI-Powered ATS Optimizer")
# st.info(
#     "You're running the fastest local development version of this app!"
# )

# Input Section
with st.container():
    col1, col2 = st.columns([1, 1])
    with col1:
        jd_input = st.text_area(
            "Paste Job Description", height=250, help="Paste the full job post here."
        )
    with col2:
        uploaded_file = st.file_uploader("Upload Current Resume (PDF)", type="pdf")

if st.button("Analyze & Optimize"):
    if uploaded_file and jd_input:
        # try:
        with st.spinner("🔍 Scanning for ATS compatibility..."):
            text = extract_text_from_pdf(uploaded_file)
            results = get_ats_analysis(text, jd_input)

            # --- NEW: HOME PAGE SCORE FIELD ---
            st.markdown("### 📊 Overall ATS Compatibility")
            col_score, col_status = st.columns([1, 2])

            with col_score:
                st.metric(label="Match Score", value=f"{results['score']}%")

            with col_status:
                status_text = (
                    "Strong Match" if results["score"] >= 70 else "Action Required"
                )
                st.subheader(f"Status: {status_text}")
                st.progress(results["score"] / 100)

            st.markdown("---")  # Visual separator

            # --- TABS AS REQUESTED ---
            t1, t2 = st.tabs(
                ["❌ Mistakes & Fixes", "🔑 Missing Keywords"]
            )

            with t1:
                st.subheader("Critical Errors")
                for error in results["formatting_issues"]:
                    st.error(error)

            with t2:
                st.subheader("Missing Technical Skills")
                st.info(", ".join(results["missing_keywords"]))

                # 5. Connect to the fixed byte-output function
                # pdf_bytes = generate_optimized_pdf(results["optimized_experience"])
                # st.download_button(
                #     label="📥 Download Optimized Resume (PDF)",
                #     data=pdf_bytes,
                #     file_name="Optimized_Resume.pdf",
                #     mime="application/pdf",
                # )

    else:
        st.error("Please provide both documents.")
