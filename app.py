from openai import OpenAI
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

st.title('📝 ResumeFit: Compare Your Resume to Job Descriptions')

with st.sidebar:
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Resume")
    resume_text = st.text_area("Paste your resume here: ", height=300)

with col2:
    st.subheader("Job Description")
    job_description_text = st.text_area("Paste the job description here: ", height=300)

compare_button = st.button("Compare")

# Function for text prepossessing
def preprocess_text(text):
    # Convert to lowercase and remove punctuation
    text = re.sub(r'[^\w\s]', '', text.lower())
    # Tokenize
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

# Function for keyword extraction and return the top 10 keywords
def extract_keywords(text, n=10):
    tokens = preprocess_text(text)
    # Count word frequencies
    word_freq = Counter(tokens)
    # Get the n most common words
    return word_freq.most_common(n)

# Function for keyword extraction and return the top 10 keywords
def compare_resume_to_job_description(resume_text, job_description_text, api_key):
    client = OpenAI(api_key=api_key)
    
    # Extract keywords from job description
    job_keywords = extract_keywords(job_description_text)
    job_keywords_str = ", ".join([f"{word} ({count})" for word, count in job_keywords])
    
    # Extract keywords from resume
    resume_keywords = extract_keywords(resume_text)
    resume_keywords_str = ", ".join([f"{word} ({count})" for word, count in resume_keywords])
    
    messages = [
        {"role": "system", "content": "You are an expert HR assistant skilled in analyzing resumes and job descriptions."},
        {"role": "user", "content": f"""Compare the following resume to the job description.
        Provide a detailed analysis of how well the candidate's qualifications match the job requirements.

        Resume: {resume_text}
        Job Description: {job_description_text}
        
        Resume Keywords: {resume_keywords_str}
        Job Description Keywords: {job_keywords_str}
        
        1. List the top 5 strengths of the candidate, explaining how each strength aligns with the job requirements.
        2. List up to 5 skill gaps or areas for improvement, suggesting ways the candidate could address these gaps.
        3. Provide a list of top 10 keywords from the job description along with their frequency. Format as 'keyword (frequency)'.
        4. Analyze the keyword match between the resume keywords and job description keywords. Discuss any significant matches or mismatches.
        5. Provide an overall qualification percentage (0-100%) and explain the rationale behind this score.
        6. Suggest 3 specific ways the candidate could improve their resume to better match this job description.

        Please provide your analysis in the following format:
        **Strengths:**
        1. [Strength 1]: [Explanation]
        2. [Strength 2]: [Explanation]
        3. [Strength 3]: [Explanation]
        4. [Strength 4]: [Explanation]
        5. [Strength 5]: [Explanation]

        Skill Gaps:
        1. [Skill Gap 1]: [Suggestion for improvement]
        2. [Skill Gap 2]: [Suggestion for improvement]
        3. [Skill Gap 3]: [Suggestion for improvement]
        4. [Skill Gap 4]: [Suggestion for improvement]
        5. [Skill Gap 5]: [Suggestion for improvement]

        Top 10 Keywords (with frequency):
        1. [Keyword 1] (frequency)
        2. [Keyword 2] (frequency)
        ...
        10. [Keyword 10] (frequency)
        
        Keyword Analysis:
        [Detailed analysis of keyword matches and mismatches]

        Overall Qualification: [XX]% \n
        Rationale: [Explanation for the qualification percentage]

        Suggestions for Resume Improvement:
        1. [Suggestion 1]
        2. [Suggestion 2]
        3. [Suggestion 3]

        Additional Comments: [Any additional analysis or comments]"""}
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0,
            max_tokens=1000,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

if compare_button:
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif not resume_text:
        st.error("Please enter your resume.")
    elif not job_description_text:
        st.error("Please enter the job description.")
    else:
        with st.spinner('Analyzing and comparing your resume to the job description...'):
            comparison_result = compare_resume_to_job_description(resume_text, job_description_text, api_key)
            if comparison_result:
                st.markdown(comparison_result)
                st.success("Analysis completed successfully")

st.sidebar.info("Note: Your API key is not stored and is only used for this session.")
st.sidebar.markdown("---")
st.sidebar.markdown("""

### How to use:
1. Paste your resume in the first box (remove your personal information).
2. Paste the job description in the second box.
3. Click 'Compare'.
4. Review the detailed analysis results.
""")
