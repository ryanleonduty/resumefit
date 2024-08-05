# 📝 ResumeFit: Compare Your Resume to Job Descriptions

ResumeFit is a Streamlit-based web application that uses AI to compare your resume against job descriptions. It provides detailed analysis and suggestions to help you tailor your resume for specific job opportunities.

## Features

- Easy-to-use interface for pasting resume and job description
- Advanced text analysis using NLTK and OpenAI's GPT-4
- Extraction of top keywords from both resume and job description
- Detailed comparison and analysis, including:
  - Top 5 strengths of the candidate
  - Up to 5 skill gaps or areas for improvement
  - Top 10 keywords from the job description with frequency
  - Keyword match analysis
  - Overall qualification percentage
  - Specific suggestions for resume improvement

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/resumefit.git
   cd resumefit
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Sign up for an OpenAI account and obtain an API key
   - You'll enter this key in the app when you run it

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to the URL provided by Streamlit (usually http://localhost:8501)

3. Enter your OpenAI API key in the sidebar

4. Paste your resume and the job description into the respective text areas

5. Click "Compare" and wait for the analysis

6. Review the detailed results and use the insights to improve your resume

## Requirements

- Python 3.7+
- Streamlit
- NLTK
- OpenAI Python Library

See `requirements.txt` for full list of dependencies.

## OpenAI API

This application does not store your resume, job descriptions, or API key. All processing is done in-memory and data is discarded after each session.
