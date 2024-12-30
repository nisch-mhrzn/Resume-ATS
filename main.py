from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import os
from PIL import Image
import io
import pdf2image
import base64
import google.generativeai as genai
from PyPDF2 import PdfReader
import re

# Configure Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
poppler_path = r"C:\poppler-24.08.0\Library\bin"


def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(
            uploaded_file.read(), poppler_path=poppler_path
        )
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("File not found")


def parse_resume_content(uploaded_file):
    # Extract text from the uploaded PDF file using PyPDF2
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Attempt to find name from the first line of the document if no "Name" field is found
    name = None
    if not re.search(r"(Name|Full Name|Candidate Name):?\s*(.*)", text, re.IGNORECASE):
        # If no name tag is found, we attempt to grab the first line from the document
        first_line = text.splitlines()[0].strip()  # 
        name = first_line

    
    name = name or "Not found"

    # Search for the email and skills in the content using regex
    email = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    skills = re.findall(r"(Skills|Technical Skills):?\s*(.*)", text, re.IGNORECASE)

    parsed_data = {
        "Name": name,
        "Email": email.group(0) if email else "Not found",
        "Skills": ", ".join([skill[1] for skill in skills]) if skills else "Not found",
    }

    return parsed_data



def highlight_keywords(resume_content, job_description):
    
    try:
        # Normalize and tokenize text
        job_keywords = set(re.findall(r"\b[a-zA-Z]+\b", job_description.lower()))
        resume_keywords = set(re.findall(r"\b[a-zA-Z]+\b", resume_content.lower()))
        
        # Filter out overly generic words (e.g., 'and', 'the')
        common_words = {"and", "the", "to", "a", "in", "of", "for", "with", "is", "on", "as", "by", "it", "at"}
        job_keywords = job_keywords - common_words
        resume_keywords = resume_keywords - common_words
        
        # Determine keyword overlap and differences
        present_keywords = job_keywords & resume_keywords
        missing_keywords = job_keywords - resume_keywords

        return present_keywords, missing_keywords
    except Exception as e:
        raise ValueError(f"Error during keyword analysis: {e}")



# Streamlit App Setup
st.set_page_config(page_title="ATS Resume Expert", page_icon="🔎", layout="wide")
st.title("🔎 ATS Resume Expert")
st.write("### Optimize your resume for Applicant Tracking Systems")

# Job Description Input

input_text = st.text_area("Enter Job Description:", key="input", height=150)

# Resume Upload Section
uploaded_file = st.file_uploader("Upload your Resume (PDF only):", type=["pdf", "txt"])
if uploaded_file is not None:
    st.success("File Uploaded Successfully")

# Buttons for Actions
col1, col2, col3 = st.columns(3)
submit1 = col1.button("Analyze Resume")
submit4 = col2.button("Percentage Match")
submit5 = col3.button("Generate Report")
# submit6 = col4.button("Extract Resume Info")

# Prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager with expertise in job roles of Python Developer, Data Science, Full Stack Web Development,Frontend Development, Backend Development, Data Engineering, DEVOPS, and Data Analysis, Cloud Computing. Review the provided resume against the job description. Provide professional evaluation on whether the candidate aligns with the role. Highlight strengths and weaknesses.
"""
input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with expertise in job roles like Python Developer, Data Science, Frontend Development, Backend Development,Web Development, Data Engineering, and DEVOPS,Data Analysis, Cloud Computing. Evaluate the resume against the job description. Provide percentage match, keywords missing, and final thoughts.
"""


def extract_pdf_text(uploaded_file):
    """
    Extract text content from a PDF file.

    Parameters:
    - uploaded_file: The uploaded PDF file.

    Returns:
    - text (str): Extracted text from the PDF.
    """
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        raise ValueError(f"Error reading PDF file: {e}")


import time

if submit1:
    if uploaded_file is not None:
        with st.spinner("Analyzing your resume..."):
            progress_bar = st.progress(0)
            
            pdf_content = input_pdf_setup(uploaded_file)
            for i in range(1, 101):
                time.sleep(0.08)  # Adjusted to slow down progress bar
                progress_bar.progress(i)
            
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            
            st.subheader("Analysis Results")
            st.write(response)
    else:
        st.error("Please upload your resume in PDF format.")

elif submit4:
    if uploaded_file is not None:
        with st.spinner("Calculating Percentage Match..."):
            progress_bar = st.progress(0)
            
            pdf_content = input_pdf_setup(uploaded_file)
            for i in range(1, 101):
                time.sleep(0.08)  # Adjusted to slow down progress bar
                progress_bar.progress(i)
            
            response = get_gemini_response(input_prompt2, pdf_content, input_text)
            
            st.subheader("Percentage Match")
            st.write(response)
    else:
        st.error("Please upload your resume in PDF format.")

elif submit5:
    if uploaded_file is not None:
        with st.spinner("Generating report..."):
            progress_bar = st.progress(0)
            
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            for i in range(1, 101):
                time.sleep(0.08)  # Adjusted to slow down progress bar
                progress_bar.progress(i)
            
           
            
            report = f"""ATS Resume Analysis Report\n\n{response}"""
            
            st.success("Report generated successfully! You can download it using the link below:")
            st.download_button("Download ATS Report", report, file_name="ATS_Report.txt", use_container_width=True)
    else:
        st.error("Please upload your resume in PDF format.")


# elif submit6:
#     if uploaded_file is not None:
#         with st.spinner("Extracting resume information..."):
#             try:
#                 progress_bar = st.progress(0)

#                 resume_text = extract_pdf_text(uploaded_file)
#                 progress_bar.progress(30)

#                 parsed_data = parse_resume_content(uploaded_file)
#                 progress_bar.progress(60)

#                 if not input_text.strip():
#                     st.error(
#                         "Please provide a valid job description or keywords for analysis."
#                     )
#                     progress_bar.progress(100)  
#                     st.stop()

               
#                 present_keywords, missing_keywords = highlight_keywords(
#                     resume_text, input_text
#                 )
#                 progress_bar.progress(100)

                
#                 st.subheader("Resume Information")
#                 st.write(parsed_data)

               
#                 st.subheader("Keyword Analysis")
#                 if present_keywords:
#                     st.write(f"**Present Keywords:** {', '.join(present_keywords)}")
#                 else:
#                     st.write("**Present Keywords:** None")

#                 if missing_keywords:
#                     st.write(f"**Missing Keywords:** {', '.join(missing_keywords)}")
#                 else:
#                     st.write("**Missing Keywords:** None")

#             except Exception as e:
#                 st.error(f"Error extracting data: {e}")
#                 progress_bar.progress(100)
#     else:
#         st.error("Please upload your resume in PDF format.")


# Footer
st.write("---")
