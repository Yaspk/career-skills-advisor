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

def get_skills_assessment(skills_data: dict) -> str:
    model = "gemini-2.5-flash-lite"
    
    prompt_text = f"""
    You are a professional skills assessment advisor. 
    Based on the following skills assessment, provide personalized recommendations:
    
    Technical Skills:
    - Programming: {skills_data['programming']}/5
    - Data Analysis: {skills_data['data_analysis']}/5
    - Design: {skills_data['design']}/5
    - Research Methods: {skills_data['research_methods']}/5
    
    Soft Skills:
    - Communication: {skills_data['communication']}/5
    - Leadership: {skills_data['leadership']}/5
    - Problem Solving: {skills_data['problem_solving']}/5
    - Teamwork: {skills_data['teamwork']}/5
    
    Career Field: {skills_data['field']}
    Current Role: {skills_data['current_role']}
    
    Please provide:
    1. A brief analysis of their current skill levels
    2. 3-4 key areas for improvement based on their field and current ratings
    3. Specific recommendations for developing each skill (1-2 suggestions per skill)
    4. A 3-month skill development plan with milestones
    
    Keep the response structured, actionable, and encouraging.
    """
    
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt_text)])]
    config = types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_budget=0))
    full_response_text = ""
    for chunk in client.models.generate_content_stream(model=model, contents=contents, config=config):
        full_response_text += chunk.text
    return full_response_text

# Page configuration
st.set_page_config(page_title="Career & Skills Advisor", page_icon="🎓", layout="wide")

# Sidebar navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
st.sidebar.title("Career Navigator")
st.sidebar.markdown("💡 Get career insights instantly—personalized for you!")

# Navigation options
page = st.sidebar.radio(
    "Navigate to:",
    ["Career Advisor", "Skills Assessment", "Learning Resources", "About"]
)

# Main content based on navigation selection
if page == "Career Advisor":
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

elif page == "Skills Assessment":
    st.title("📊 Skills Assessment")
    st.write("Evaluate your current skills and identify areas for improvement.")
    
    # Get user context
    col1, col2 = st.columns(2)
    with col1:
        current_role = st.selectbox("Current Role/Position", [
            "Student", "Entry-level Professional", "Mid-level Professional", 
            "Senior Professional", "Manager", "Executive", "Career Changer"
        ])
    
    with col2:
        field = st.selectbox("Career Field/Industry", [
            "Technology", "Business", "Healthcare", "Creative Arts", 
            "Science & Research", "Education", "Engineering", "Marketing"
        ])
    
    st.subheader("Rate your proficiency in these areas (1-5):")
    
    technical_skills = st.expander("Technical Skills", expanded=True)
    with technical_skills:
        programming = st.slider("Programming", 1, 5, 3, 
                              help="Ability to write and understand code")
        data_analysis = st.slider("Data Analysis", 1, 5, 3, 
                                 help="Ability to work with data, statistics, and analytics")
        design = st.slider("Design", 1, 5, 3, 
                          help="Visual design, UX/UI, or creative skills")
        research_methods = st.slider("Research Methods", 1, 5, 3, 
                                    help="Research, analysis, and investigative skills")
    
    soft_skills = st.expander("Soft Skills", expanded=True)
    with soft_skills:
        communication = st.slider("Communication", 1, 5, 3, 
                                 help="Verbal, written, and presentation skills")
        leadership = st.slider("Leadership", 1, 5, 3, 
                              help="Ability to guide, motivate, and manage others")
        problem_solving = st.slider("Problem Solving", 1, 5, 3, 
                                   help="Analytical thinking and creative solution development")
        teamwork = st.slider("Teamwork", 1, 5, 3, 
                            help="Collaboration and interpersonal skills")
    
    if st.button("Get Skills Assessment", type="primary"):
        with st.spinner("Analyzing your skills profile..."):
            skills_data = {
                "programming": programming,
                "data_analysis": data_analysis,
                "design": design,
                "research_methods": research_methods,
                "communication": communication,
                "leadership": leadership,
                "problem_solving": problem_solving,
                "teamwork": teamwork,
                "field": field,
                "current_role": current_role
            }
            
            assessment = get_skills_assessment(skills_data)
        
        st.success("Here's your personalized skills assessment!")
        st.markdown(assessment)
        
        # Additional visualization
        st.subheader("Skills Profile Overview")
        
        # Create a simple radar chart data representation
        categories = ['Programming', 'Data Analysis', 'Design', 'Research', 
                     'Communication', 'Leadership', 'Problem Solving', 'Teamwork']
        values = [programming, data_analysis, design, research_methods, 
                 communication, leadership, problem_solving, teamwork]
        
        # Display as metrics
        cols = st.columns(4)
        for i, (category, value) in enumerate(zip(categories, values)):
            with cols[i % 4]:
                st.metric(category, f"{value}/5")

elif page == "Learning Resources":
    st.title("📚 Learning Resources")
    st.write("Discover resources to develop your skills and advance your career.")
    
    resource_type = st.selectbox("Select resource type:", 
                                ["Online Courses", "Books", "Tutorials", "Certifications"])
    
    field = st.selectbox("Select field:", 
                        ["Technology", "Business", "Healthcare", "Creative Arts", "Science"])
    
    if st.button("Find Resources"):
        st.info("Resource recommendation feature coming soon! This will provide curated learning materials based on your interests.")

elif page == "About":
    st.title("ℹ️ About Career Navigator")
    st.write("""
    Career Navigator is an AI-powered platform designed to help students and professionals 
    explore career options, assess their skills, and discover learning resources.
    
    ### How it works:
    - Get personalized career advice based on your education, interests, and skills
    - Assess your current skill levels and identify areas for improvement
    - Discover curated learning resources to help you grow
    
    ### Our mission:
    To make career guidance accessible and personalized for everyone, 
    helping you navigate your professional journey with confidence.
    """)
    
    st.subheader("Contact Us")
    st.write("Have questions or feedback? We'd love to hear from you!")
    st.write("Email: contact@careernavigator.example")
    st.write("Twitter: @CareerNav")

# Footer
st.markdown("""---  
Made with ❤ to help you grow. Explore, dream, and achieve!  
""")
