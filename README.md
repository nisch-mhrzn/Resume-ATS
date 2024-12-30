# ATS Resume Expert

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Completed-success?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/nisch-mhrzn/Resume-ATS?style=flat-square)
![Repo Size](https://img.shields.io/github/repo-size/nisch-mhrzn/Resume-ATS?style=flat-square)

## Overview
ATS Resume Expert is a powerful Streamlit-based application designed to optimize resumes for Applicant Tracking Systems (ATS). The app allows users to analyze their resumes against job descriptions, providing detailed feedback, keyword matching, and a professional evaluation.

## Features
- **Resume Analysis:** Compare your resume with a job description and receive professional feedback on strengths and weaknesses.
- **Percentage Match:** Analyze the alignment between your resume and the job description, including keyword presence and missing keywords.
- **Downloadable Reports:** Generate and download a detailed report of the analysis.
- **Resume Parsing:** Extract structured data such as name, email, and skills from the uploaded resume.
- **Real-Time Keyword Highlighting:** Identify keywords from the job description that are present or missing in the resume.

## Technologies Used
- **Python**
- **Streamlit**
- **Google Generative AI API**
- **pdf2image** for PDF processing
- **re** for regular expressions
- **dotenv** for managing environment variables

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/nisch-mhrzn/Resume-ATS.git
   cd Resume-ATS
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory.
   - Add your Google API Key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

4. Install [Poppler](http://blog.alivate.com.au/poppler-windows/) for PDF conversion and add its bin folder to your system's PATH.

## Usage
1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open the app in your browser (default: `http://localhost:8501`).

3. Upload your resume and enter the job description to begin analysis.

## How It Works
1. **Resume Analysis:** Uses Google Generative AI to evaluate resumes and provide professional insights.
2. **Keyword Matching:** Compares job description keywords with resume content to highlight present and missing keywords.
3. **Parsing & Report:** Extracts structured data and generates a detailed analysis report.

## Screenshots
### Home Page
![Home Page]()

### Analysis Results
![Analysis Results]()

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Open a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
For inquiries or support, please contact [Nischal Maharjan](mailto:nischal.maharjan1233@gmail.com).

