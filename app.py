import os
import streamlit as st
from google import genai
from google.genai import types

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("API key not found. Please set the GEMINI_API_KEY environment variable.")
    st.stop()

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

# Dynamic widgets (NO st.form)
name = st.text_input("👤 Your Name")
education_level = st.selectbox("🎓 Education Level", ["High School", "Undergraduate", "Postgraduate", "Others"])

if education_level == "High School":
    interests = st.text_area("✨ What subjects or activities do you enjoy most?", placeholder="e.g., science fairs, maths, writing, robotics, debate")
    skills_have = st.text_area("💪 What are your strengths or talents?", placeholder="e.g., teamwork, coding, creative writing, public speaking")
    skills_want = st.text_area("🚀 Skills or topics you'd like to explore next?", placeholder="e.g., web design, debating, photography, coding")
    hobbies = st.text_area("🎲 Activities or projects you enjoy?", placeholder="e.g., chess club, painting, music, science projects, volunteering")
elif education_level == "Undergraduate":
    interests = st.text_area("✨ Majors, projects, or subjects you're most passionate about?", placeholder="e.g., economics, app development, AI research, entrepreneurship")
    skills_have = st.text_area("💪 Strengths and abilities (technical or soft skills)?", placeholder="e.g., Java, Python, data analysis, leadership, presentations")
    skills_want = st.text_area("🚀 Skills or tools you're eager to learn for jobs/internships?", placeholder="e.g., cloud computing, machine learning, digital marketing, Excel")
    hobbies = st.text_area("🎲 Campus activities, competitions, or events you take part in?", placeholder="e.g., music band, sports team, case comps, hackathons, volunteering")
elif education_level == "Postgraduate":
    interests = st.text_area("✨ Research areas or industries that interest you?", placeholder="e.g., AI research, consulting, biotech, publications")
    skills_have = st.text_area("💪 Advanced skills, methods, or expertise you have?", placeholder="e.g., machine learning, academic writing, teaching, lab techniques")
    skills_want = st.text_area("🚀 Skills you'd like to acquire for career growth?", placeholder="e.g., leadership, Python for data science, research methods")
    hobbies = st.text_area("🎲 Ways you build creativity or recharge?", placeholder="e.g., blogging, travel, music, sports, photography")
else:
    interests = st.text_area("✨ Interests or industries you're considering?", placeholder="e.g., business, design, teaching, government jobs, freelancing")
    skills_have = st.text_area("💪 Current skills from any context (school, job, self-taught)?", placeholder="e.g., Excel, negotiation, creative writing, management")
    skills_want = st.text_area("🚀 Skills you want to gain for new opportunities?", placeholder="e.g., public speaking, coding, digital marketing, leadership")
    hobbies = st.text_area("🎲 Activities or projects you enjoy?", placeholder="e.g., theatre, gaming, social work, travel, writing")

if st.button("🔎 Show Me My Career Advice!"):
    if not (name and education_level and interests and skills_have and skills_want and hobbies):
        st.warning("Please fill in all fields for the best advice.")
    else:
        prompt = (
            f"You are a professional career advisor. "
            f"My name is {name}. I am currently a {education_level} student. "
            f"My interests are: {interests}. "
            f"My skills (strengths/talents): {skills_have}. "
            f"I want to learn/explore: {skills_want}. "
            f"My hobbies or key activities: {hobbies}. "
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
