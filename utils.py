import google.generativeai as genai
import pdfplumber
import os
import json
from dotenv import load_dotenv
from fpdf import FPDF
import streamlit as st

# Load API key from streamlit secrets

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def extract_text_from_pdf(uploaded_file):
    """
    pdfplumber is better at handling
    complex resume layouts (columns/tables).
    """
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# Change this to False when you want to use the real AI
MOCK_MODE = False

def get_ats_analysis(resume_text, job_description):
    if MOCK_MODE:
        # Fake data that looks like the real AI response
        return {
            "score": 85,
            "summary": "Mock Analysis: This is a placeholder to help you design your UI without hitting API limits.",
            "missing_keywords": ["Python", "Cloud Architecture", "SQL"],
            "formatting_issues": ["Columns found in resume", "Images present"],
            "optimized_experience": "Developed scalable data pipelines using Python and AWS... (Mock Optimized Text)",
        }

    """
    Sends data to Gemini and forces a JSON response.
    """
    model = genai.GenerativeModel("models/gemini-3-flash-preview")

    prompt = f"""
    Act as a professional ATS (Applicant Tracking System) and Senior Technical Recruiter.
    Analyze the following Resume against the Job Description (JD).
    Resume Text: {resume_text}
    Job Description: {job_description}
    You MUST respond ONLY in valid JSON format with the following keys:
    1. "score": (An integer from 0-100)
    2. "summary": (A 2-sentence overview of the candidate's fit)
    3. "missing_keywords": (A list of skills/tools mentioned in JD but missing in Resume)
    4. "formatting_issues": (List any issues like tables, columns, or images that confuse ATS)
    5. "optimized_experience": (A rewritten 'Experience' bullet point for the user to copy)
    """

    response = model.generate_content(prompt)

    # We strip any potential markdown backticks from the AI response
    clean_json = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)

