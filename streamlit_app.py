import streamlit as st
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from openai import OpenAI
import traceback

# Hardcoded API key
GEMINI_API_KEY = input()

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'client' not in st.session_state:
    st.session_state.client = OpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

# Custom CSS for centering and white result box
st.markdown("""
<style>
    .centered-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background: #181c24;
    }
    .system-role {
        background: #e3f0ff;
        color: #1f77b4;
        padding: 18px 32px;
        border-radius: 10px;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        max-width: 700px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        font-weight: 500;
    }
    .white-box {
        background: #fff;
        color: #222;
        padding: 24px 32px;
        border-radius: 10px;
        margin-top: 2rem;
        max-width: 700px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        font-size: 1.1rem;
        word-break: break-word;
    }
    .input-box {
        width: 100%;
        max-width: 700px;
        margin-bottom: 1.5rem;
    }
    .submit-btn {
        width: 100%;
        max-width: 700px;
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 8px;
        background: #007bff;
        color: #fff;
        border: none;
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
        cursor: pointer;
        transition: background 0.2s;
    }
    .submit-btn:hover {
        background: #0056b3;
    }
</style>
<div class="centered-container">
""", unsafe_allow_html=True)

# Fetch data if not already loaded
if st.session_state.data is None:
    try:
        base_url = "https://sarkariresult.com.cm/"
        with urlopen(base_url, timeout=10) as response:
            html = response.read().decode('utf-8')
        mysoup = BeautifulSoup(markup=html, features="html.parser")
        if mysoup.body:
            st.session_state.data = mysoup.body.get_text(strip=True, separator="\n")
        else:
            st.session_state.data = "No body content found"
    except Exception as e:
        st.session_state.data = "Error fetching website data"

# System role prompt
truncated_data = st.session_state.data[:8000] if len(st.session_state.data) > 8000 else st.session_state.data
system_role = f"You are an AI Assistant specialized in government exams and job opportunities. Here is the latest exam information: [data loaded from sarkariresult.com.cm]"
st.markdown(f'<div class="system-role"><b>System Role:</b> {system_role}</div>', unsafe_allow_html=True)

# User input
with st.form("ask_form", clear_on_submit=False):
    user_question = st.text_area(
        "What would you like to know about government exams?",
        placeholder="e.g., What are the latest government job opportunities?",
        height=100,
        key="user_question",
        help="Type your question and press Submit."
    )
    submitted = st.form_submit_button("Submit", use_container_width=True)

# Result output
if submitted and user_question.strip():
    with st.spinner("🔄 Fetching latest exam information..."):
        try:
            mymsg = [
                {"role": "system", "content": f"You are an AI Assistant specialized in government exams and job opportunities. Here is the latest exam information: {truncated_data}"},
                {"role": "user", "content": user_question}
            ]
            response = st.session_state.client.chat.completions.create(
                model="gemini-2.0-flash",
                messages=mymsg
            )
            result = response.choices[0].message.content
            st.markdown(f'<div class="white-box">{result}</div>', unsafe_allow_html=True)
        except (URLError, HTTPError) as e:
            st.markdown(f'<div class="white-box">❌ Network Error: {e}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<div class="white-box">❌ Error: {e}</div>', unsafe_allow_html=True)
            st.code(traceback.format_exc())

st.markdown("</div>", unsafe_allow_html=True) 
