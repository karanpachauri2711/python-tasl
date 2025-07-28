# mcq_generator_app.py

import os
import requests
import streamlit as st
from typing import List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ===============================
# Function 1: Extract YouTube Transcript
# ===============================
def extract_youtube_transcript(video_url: str) -> str:
    try:
        video_id = get_video_id(video_url)
        if not video_id:
            return ""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
        return " ".join([entry['text'] for entry in transcript])
    except Exception:
        return ""

# ===============================
# Helper Function to Extract Video ID
# ===============================
def get_video_id(video_url: str) -> str:
    parsed = urlparse(video_url)
    if 'youtube.com' in parsed.netloc:
        return parse_qs(parsed.query).get('v', [None])[0]
    elif 'youtu.be' in parsed.netloc:
        return parsed.path.lstrip('/')
    return None

# ===============================
# Function 2: Extract Transcript from URL
# ===============================
def extract_transcript_from_url(video_url: str) -> str:
    if 'youtube.com' in video_url or 'youtu.be' in video_url:
        return extract_youtube_transcript(video_url)
    else:
        headers = {"authorization": os.getenv("API_KEY")}
        transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
        response = requests.post(transcript_endpoint, json={"audio_url": video_url}, headers=headers)
        transcript_id = response.json().get("id")

        polling_endpoint = f"{transcript_endpoint}/{transcript_id}"
        while True:
            polling_response = requests.get(polling_endpoint, headers=headers).json()
            if polling_response["status"] == "completed":
                return polling_response["text"]
            elif polling_response["status"] == "error":
                return ""

# ===============================
# Function 3: Extract Transcript (Main Entry)
# ===============================
def extract_transcript(video_path: str) -> str:
    if video_path.startswith("http"):
        return extract_transcript_from_url(video_path)
    else:
        try:
            import whisper
            model = whisper.load_model("base")
            result = model.transcribe(video_path)
            return result['text']
        except:
            return ""

# ===============================
# Function 4: YouTube Title & Description
# ===============================
def get_youtube_title_description(video_url: str) -> str:
    video_id = get_video_id(video_url)
    if not video_id:
        return "Invalid YouTube URL. Cannot extract video ID."
    api_key = os.getenv("YOUTUBE_API_KEY")
    if api_key:
        endpoint = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
        response = requests.get(endpoint).json()
        items = response.get("items")
        if items:
            snippet = items[0]['snippet']
            return snippet['title'] + "\n" + snippet.get('description', '')
    response = requests.get(f"https://www.youtube.com/oembed?url={video_url}&format=json")
    if response.status_code == 200:
        return response.json().get("title", "")
    return ""

# ===============================
# Function 5: Generate MCQ via Gemini
# ===============================
def generate_mcq_gemini(transcript: str, num_questions: int = 5, language: str = "en") -> Dict[str, List[str]]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('GEMINI_API_KEY')}"
    }
    prompt = f"""
    Generate {num_questions} multiple choice questions in {language} based on the following content:
    ```{transcript}```
    Return the result as a JSON object with question as key and value as a list of 4 options followed by the correct answer.
    """
    response = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent", 
                             headers=headers, 
                             json={"contents": [{"parts": [{"text": prompt}]}]})
    try:
        text = response.json()['candidates'][0]['content']['parts'][0]['text']
        return eval(text)
    except:
        return {}

# ===============================
# Function 6: Generate MCQs in Both Languages
# ===============================
def generate_mcq_from_video_both_languages(video_path: str, num_questions: int = 5) -> Dict[str, Dict[str, List[str]]]:
    transcript = extract_transcript(video_path)
    if not transcript:
        transcript = get_youtube_title_description(video_path)
    return {
        "English": generate_mcq_gemini(transcript, num_questions=num_questions, language="en"),
        "Hindi": generate_mcq_gemini(transcript, num_questions=num_questions, language="hi")
    }

# ===============================
# Streamlit Frontend
# ===============================
st.title("📽️ YouTube Video to MCQ Quiz")
video_url = st.text_input("Enter YouTube or direct video URL:")
num_qs = st.slider("Number of MCQs", 1, 10, 5)

if st.button("Generate Quiz") and video_url:
    with st.spinner("Generating MCQs..."):
        mcqs = generate_mcq_from_video_both_languages(video_url, num_questions=num_qs)

    for lang, questions in mcqs.items():
        st.header(f"{lang} Questions")
        for q, opts in questions.items():
            user_ans = st.radio(q, opts[:-1], key=q+lang)
            if st.button(f"Submit Answer ({lang})", key=f"{q}_submit_{lang}"):
                if user_ans == opts[-1]:
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. Correct answer: {opts[-1]}")
