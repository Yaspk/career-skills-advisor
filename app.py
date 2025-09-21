import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from google import genai
from google.genai import types

# --- API Configuration ---
# You can set this as a Streamlit Secret or an environment variable.
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("API key not found. Please set the 'GEMINI_API_KEY' environment variable.")
    st.stop()

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Failed to initialize Gemini client: {e}")
    st.stop()

# --- Core LLM Functions (Corrected and Refined) ---

def get_career_advice_stream(prompt_text: str) -> str:
    """
    Generates a career advice response in a streaming fashion.
    
    The 'thinking_config' parameter was removed as it is not a valid
    argument for the streaming API and was causing a runtime error.
    """
    model = "gemini-2.5-flash-lite"
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt_text)])]
    
    full_response_text = ""
    # Use st.empty() to create a container for live updates.
    message_placeholder = st.empty()
    
    try:
        for chunk in client.models.generate_content_stream(model=model, contents=contents):
            full_response_text += chunk.text
            # Append the new chunk to the placeholder to create a streaming effect
            message_placeholder.markdown(full_response_text + "▌") 
    except Exception as e:
        full_response_text = f"An error occurred: {e}"
    
    message_placeholder.markdown(full_response_text)
    return full_response_text

def get_skills_assessment(skills_data: dict) -> str:
    """
    Generates a personalized skills assessment report.
    
    The 'thinking_config' parameter was also removed from this function.
    """
    model = "gemini-2.5-flash-lite"
    
    # Build skills string for the prompt
    skills_str = "Technical Skills:\n"
    for skill, value in skills_data['technical_skills'].items():
        skills_str += f"- {skill}: {value}/5\n"
    
    skills_str += "\nSoft Skills:\n"
    for skill, value in skills_data['soft_skills'].items():
        skills_str += f"- {skill}: {value}/5\n"
    
    prompt_text = f"""
    You are a professional skills assessment advisor for Indian students and young professionals. 
    Based on the following skills assessment, provide a personalized and encouraging
    analysis to help them navigate the Indian job market.
    
    {skills_str}
    
    Career Field: {skills_data['field']}
    Current Role: {skills_data['current_role']}
    
    Please provide:
    1. A brief, encouraging analysis of their current skill levels in the context of their chosen field.
    2. 3-4 key areas for improvement, specifically referencing both technical and soft skills.
    3. Specific, actionable recommendations for developing each skill, including online courses, platforms, or project ideas relevant to the Indian context (e.g., platforms like Coursera, Udemy, or NPTEL).
    4. A 3-month skill development plan with clear, achievable milestones.
    
    Keep the response structured, actionable, and encouraging, formatted using Markdown.
    """
    
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt_text)])]
    full_response_text = ""
    message_placeholder = st.empty()
    
    try:
        for chunk in client.models.generate_content_stream(model=model, contents=contents):
            full_response_text += chunk.text
            message_placeholder.markdown(full_response_text + "▌")
    except Exception as e:
        full_response_text = f"An error occurred: {e}"
        
    message_placeholder.markdown(full_response_text)
    return full_response_text

def get_learning_resources(field: str, resource_type: str) -> str:
    """Generates a list of learning resources based on user's field and resource type."""
    model = "gemini-2.5-flash-lite"
    
    prompt_text = f"""
    You are a career development expert specializing in the Indian education system.
    Provide a list of 5 key {resource_type} for someone looking to build a career in the "{field}" field.
    The recommendations should be highly relevant to students in India and include a brief description of each resource.
    For online courses, mention platforms like Coursera, edX, or NPTEL. For books, mention classic and modern titles.
    Format your response as a clear, easy-to-read Markdown list with titles, descriptions, and an encouraging opening sentence.
    """
    
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt_text)])]
    full_response_text = ""
    message_placeholder = st.empty()
    
    try:
        for chunk in client.models.generate_content_stream(model=model, contents=contents):
            full_response_text += chunk.text
            message_placeholder.markdown(full_response_text + "▌")
    except Exception as e:
        full_response_text = f"An error occurred: {e}"
        
    message_placeholder.markdown(full_response_text)
    return full_response_text

def get_field_specific_skills(field: str) -> list:
    """Return field-specific technical skills"""
    field_skills = {
        "Technology": [
            "Programming (Python, Java)", "Data Structures & Algorithms", "Cloud Computing (AWS/GCP/Azure)", 
            "DevOps", "Cybersecurity", "UI/UX Design", "Machine Learning"
        ],
        "Business": [
            "Financial Analysis", "Market Research", "Strategic Planning", 
            "Project Management", "Business Development", "Data Analysis", "CRM Software"
        ],
        "Healthcare": [
            "Patient Care", "Medical Terminology", "Clinical Procedures", 
            "Healthcare IT", "Medical Documentation", "Diagnostic Tools", "Pharmaceutical Knowledge"
        ],
        "Creative Arts": [
            "Graphic Design", "Video Editing", "Photography", 
            "Illustration", "3D Modeling", "Typography", "Color Theory"
        ],
        "Science & Research": [
            "Laboratory Techniques", "Statistical Analysis", "Research Methodology", 
            "Scientific Writing", "Data Interpretation", "Experimental Design", "Literature Review"
        ],
        "Education": [
            "Curriculum Development", "Classroom Management", "Educational Technology", 
            "Assessment Design", "Differentiated Instruction", "Student Engagement", "Lesson Planning"
        ],
        "Engineering": [
            "CAD Software", "Technical Drawing", "Systems Design", 
            "Quality Control", "Manufacturing Processes", "Structural Analysis", "Project Management"
        ],
        "Marketing": [
            "Digital Marketing", "SEO/SEM", "Content Creation", 
            "Social Media Management", "Market Analysis", "Brand Management", "Analytics Tools"
        ],
        "Data Science": [
            "Statistical Modeling", "Python/R", "Data Visualization",
            "Machine Learning", "Big Data (Hadoop/Spark)", "SQL", "Data Cleaning & Wrangling"
        ]
    }
    
    return field_skills.get(field, [
        "Problem Solving", "Technical Aptitude", "Analytical Thinking", 
        "Tool Proficiency", "Industry Knowledge", "Technical Writing"
    ])

# --- Visualization Functions ---

def create_radar_chart(technical_skills: dict, soft_skills: dict) -> go.Figure:
    """Create a radar chart visualization of skills"""
    categories = list(technical_skills.keys()) + list(soft_skills.keys())
    values = list(technical_skills.values()) + list(soft_skills.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Skills Assessment',
        line=dict(color='#3498db'),
        marker=dict(size=10, symbol='circle')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['1', '2', '3', '4', '5'],
                gridcolor='#bdc3c7'
            ),
            bgcolor='#f5f5f5'
        ),
        showlegend=False,
        title_text="<b style='color:#2c3e50;'>Skills Radar Chart</b>",
        height=500,
        font=dict(family="Arial, sans-serif")
    )
    
    return fig

def create_bar_chart(technical_skills: dict, soft_skills: dict, field: str) -> px.bar:
    """Create a bar chart visualization of skills"""
    # Combine skills
    all_skills = {**technical_skills, **soft_skills}
    
    # Create DataFrame for plotting
    df = pd.DataFrame({
        'Skill': list(all_skills.keys()),
        'Rating': list(all_skills.values()),
        'Type': ['Technical'] * len(technical_skills) + ['Soft'] * len(soft_skills)
    })
    
    # Sort by rating for better visualization
    df = df.sort_values(by='Rating', ascending=False)
    
    # Create plot
    fig = px.bar(
        df, 
        x='Skill', 
        y='Rating', 
        color='Type',
        title=f"<b>Skills Assessment for {field}</b>",
        labels={'Skill': 'Skill Area', 'Rating': 'Proficiency Level (1-5)'},
        color_discrete_map={'Technical': '#3498db', 'Soft': '#2ecc71'},
        text_auto=True
    )
    
    fig.update_layout(
        yaxis_range=[0,5],
        title_x=0.5,
        font=dict(family="Arial, sans-serif"),
        plot_bgcolor='#f5f5f5',
        xaxis={'categoryorder':'total descending'}
    )
    
    return fig

# --- Main Streamlit Application UI ---

st.set_page_config(page_title="Career Navigator", page_icon="🎓", layout="wide")

# Sidebar navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("Career Navigator")
    st.markdown("💡 Get personalized career insights and skill advice powered by AI!")
    st.markdown("---")
    page = st.radio(
        "Navigate to:",
        ["Career Advisor", "Skills Assessment", "Learning Resources", "About"]
    )
    st.markdown("---")
    st.markdown("Made with ❤️ to help you grow. Explore, dream, and achieve!")

# Main content based on navigation selection
if page == "Career Advisor":
    st.title("🌟 Personalized Career Advisor")
    st.write("Tell me about yourself, and I'll help you explore your future career options and skill development ideas relevant to the Indian job market!")
    st.markdown("---")
    
    # Dynamic widgets (NO st.form)
    with st.container(border=True):
        st.subheader("Your Profile")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Your Name", placeholder="e.g., Priya Sharma")
        with col2:
            education_level = st.selectbox("🎓 Education Level", ["High School", "Undergraduate", "Postgraduate", "Professional", "Other"])
        
        interests = st.text_area("✨ What subjects, industries, or activities are you passionate about?", placeholder="e.g., mathematics, artificial intelligence, healthcare, entrepreneurship, sustainable energy")
        skills_have = st.text_area("💪 What are your current strengths or talents (technical or soft skills)?", placeholder="e.g., Python, data analysis, public speaking, teamwork, financial modeling")
        skills_want = st.text_area("🚀 What skills or topics are you eager to learn or explore next?", placeholder="e.g., cloud computing, digital marketing, graphic design, leadership, UX/UI")

    if st.button("🔎 Get Personalized Career Advice!", use_container_width=True, type="primary"):
        if not (name and education_level and interests and skills_have and skills_want):
            st.warning("Please fill in all fields to get the best advice.")
        else:
            prompt = (
                f"You are a professional career advisor for young people in India. "
                f"My name is {name}. My education level is {education_level}. "
                f"My interests are: {interests}. "
                f"My current skills (strengths/talents): {skills_have}. "
                f"I want to learn/explore: {skills_want}. "
                "Please give me warm, encouraging, friendly, and personalized guidance. "
                "List 2-4 matching career domains with descriptions. For each domain, "
                "outline the key skills one should develop and suggest 1-2 learning resources or "
                "project ideas. The advice should be tailored to the Indian context and evolving job market. "
                "Conclude with a motivational tip."
            )
            with st.spinner("Thinking about your best career matches..."):
                advice = get_career_advice_stream(prompt)

elif page == "Skills Assessment":
    st.title("📊 Skills Assessment")
    st.write("Evaluate your current skills and identify areas for improvement. Get a detailed report and development plan.")
    st.markdown("---")
    
    # Get user context
    with st.container(border=True):
        st.subheader("Your Professional Context")
        col1, col2 = st.columns(2)
        with col1:
            current_role = st.selectbox("Current Role/Position", [
                "Student", "Entry-level Professional", "Mid-level Professional", 
                "Senior Professional", "Manager", "Executive", "Career Changer"
            ])
        with col2:
            field = st.selectbox("Career Field/Industry", [
                "Technology", "Business", "Healthcare", "Creative Arts", 
                "Science & Research", "Education", "Engineering", "Marketing", "Data Science"
            ])
            
    st.subheader("Rate your proficiency (1-5)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<b>Technical Skills</b>", unsafe_allow_html=True)
        technical_skills_list = get_field_specific_skills(field)
        technical_ratings = {skill: st.slider(skill, 1, 5, 3, key=f"tech_{skill}") for skill in technical_skills_list}

    with col2:
        st.markdown("<b>Soft Skills</b>", unsafe_allow_html=True)
        soft_skills_list = [
            "Communication", "Leadership", "Problem Solving", "Teamwork", 
            "Adaptability", "Time Management", "Creativity"
        ]
        soft_ratings = {skill: st.slider(skill, 1, 5, 3, key=f"soft_{skill}") for skill in soft_skills_list}

    if st.button("📈 Get Skills Assessment & Report", use_container_width=True, type="primary"):
        skills_data = {
            "technical_skills": technical_ratings,
            "soft_skills": soft_ratings,
            "field": field,
            "current_role": current_role
        }
        
        with st.spinner("Analyzing your skills profile..."):
            assessment = get_skills_assessment(skills_data)
        
        st.success("Here's your personalized skills assessment!")
        st.markdown(assessment)
        
        st.markdown("---")
        st.subheader("Skills Visualization")
        
        vis_col1, vis_col2 = st.columns([1, 1])
        with vis_col1:
            st.plotly_chart(create_radar_chart(technical_ratings, soft_ratings), use_container_width=True)
        with vis_col2:
            st.plotly_chart(create_bar_chart(technical_ratings, soft_ratings, field), use_container_width=True)
        
        st.markdown("---")
        st.subheader("Skills Summary Table")
        
        all_skills = {**technical_ratings, **soft_ratings}
        skills_df = pd.DataFrame({
            'Skill': list(all_skills.keys()),
            'Rating': list(all_skills.values()),
            'Type': ['Technical'] * len(technical_ratings) + ['Soft'] * len(soft_ratings)
        })
        
        def get_rating_category(rating):
            if rating <= 2:
                return "Needs Improvement"
            elif rating == 3:
                return "Intermediate"
            else:
                return "Advanced"
        
        skills_df['Level'] = skills_df['Rating'].apply(get_rating_category)
        
        st.dataframe(
            skills_df,
            column_config={
                "Skill": "Skill",
                "Rating": st.column_config.ProgressColumn(
                    "Rating",
                    format="%d",
                    min_value=1,
                    max_value=5,
                ),
                "Type": "Type",
                "Level": "Proficiency Level"
            },
            hide_index=True,
            use_container_width=True
        )

elif page == "Learning Resources":
    st.title("📚 Learning Resources")
    st.write("Discover curated resources to develop your skills and advance your career.")
    st.markdown("---")
    
    with st.container(border=True):
        st.subheader("Find Resources")
        col1, col2 = st.columns(2)
        with col1:
            field = st.selectbox("Select your field:", [
                "Technology", "Business", "Healthcare", "Creative Arts", 
                "Science & Research", "Education", "Engineering", "Marketing", "Data Science"
            ])
        with col2:
            resource_type = st.selectbox("Select resource type:", 
                                         ["Online Courses", "Books", "Tutorials", "Certifications"])
        
    if st.button("📖 Find Resources!", use_container_width=True, type="primary"):
        with st.spinner(f"Finding relevant {resource_type} for {field}..."):
            get_learning_resources(field, resource_type)

elif page == "About":
    st.title("ℹ️ About Career Navigator")
    st.write("Career Navigator is an AI-powered platform designed to help students and professionals in India explore career options, assess their skills, and discover learning resources relevant to the evolving job market.")
    st.markdown("""
    ### Our Approach
    We believe that generic career advice is no longer enough. Our platform uses Google's powerful generative AI to create a dynamic, personalized experience that adapts to your unique profile. By analyzing your interests, existing skills, and career goals, we provide insights that are not only relevant but also actionable.
    

    ### How It Works
    * **Career Advisor:** Get a personalized roadmap with potential career paths based on your interests and skills.
    * **Skills Assessment:** Evaluate your proficiency in both technical and soft skills, complete with visual charts and a detailed development plan.
    * **Learning Resources:** Find curated recommendations for online courses, certifications, and books tailored to your field of interest.

    Our mission is to empower you to navigate your professional journey with confidence and clarity, helping you bridge the gap between education and a fulfilling career.
    """)
    
    st.subheader("Contact Us")
    st.write("Have questions or feedback? We'd love to hear from you! Email: contact@careernavigator.example")
