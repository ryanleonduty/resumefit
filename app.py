from openai import OpenAI
import streamlit as st
import spacy
from collections import Counter
import re

# Load spaCy model
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

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

# Function for text preprocessing
def preprocess_text(text):
    # Convert to lowercase and remove punctuation
    text = re.sub(r'[^\w\s]', '', text.lower())
    # Process with spaCy
    doc = nlp(text)
    # Remove stopwords and return lemmatized tokens
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return tokens

# Function for keyword extraction and return the top 10 keywords
def extract_keywords(text, n=10):
    tokens = preprocess_text(text)
    # Count word frequencies
    word_freq = Counter(tokens)
    # Get the n most common words
    return word_freq.most_common(n)

# Rest of your code (compare_resume_to_job_description function, etc.) remains the same

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
