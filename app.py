import os
import streamlit as st
from google import genai
from google.genai import types

# Load Gemini API Key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("API key not found. Please set the GEMINI_API_KEY environment variable.")
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

def get_career_advice_stream(prompt_text: str) -> str:
    model = "gemini-2.5-flash-lite"
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt_text)])]
    config = types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_budget=0))
    full_response_text = ""
    for chunk in client.models.generate_content_stream(model=model, contents=contents, config=config):
        full_response_text += chunk.text
    return full_response_text

st.set_page_config(page_title="Career & Skills Advisor", page_icon="🎓", layout="wide")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
st.sidebar.title("Career Navigator")
st.sidebar.markdown("💡 Get career insights instantly—personalized for you!")

st.title("🌟 Personalized Career & Skills Advisor")
st.write("Tell me about yourself and I'll help you explore your future career options and skill development ideas!")

with st.form("career_input_form"):
    name = st.text_input("👤 Your Name")
    education_level = st.selectbox("🎓 Education Level", ["High School", "Undergraduate", "Postgraduate", "Others"])
    interests = st.text_area("✨ Interests or favorite subjects", placeholder="e.g., coding, writing, biology, music...")
    skills_have = st.text_area("💪 Skills you have", placeholder="e.g., Python, teamwork, communication...")
    skills_want = st.text_area("🚀 Skills you want to learn", placeholder="e.g., AI, marketing, design...")
    hobbies = st.text_area("🎲 Hobbies that make you happy", placeholder="e.g., chess, painting, music...")

    submitted = st.form_submit_button("🔎 Show Me My Career Advice!")

if submitted:
    if not (name and education_level and interests and skills_have and skills_want and hobbies):
        st.warning("Please fill in all fields for the best advice.")
    else:
        prompt = (
            f"You are a professional career advisor. "
            f"My name is {name}. I am currently a {education_level} student. "
            f"My interests are: {interests}. "
            f"My current skills are: {skills_have}. "
            f"I want to learn: {skills_want}. "
            f"My hobbies are: {hobbies}. "
            "Please give me warm, encouraging, friendly, and personalized guidance. "
            "List 2-4 matching career domains with descriptions, "
            "skills I should develop, and 1-2 learning resources or project ideas for each. "
            "Conclude with a motivational tip."
        )
        with st.spinner("Thinking about your best career matches..."):
            advice = get_career_advice_stream(prompt)
        st.success("Here's your personalized career guidance!")
        st.markdown(advice)

st.markdown("""---  
Made with ❤ to help you grow. Explore, dream, and achieve!  
""")