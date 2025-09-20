# Personalized Career & Skills Advisor

A Streamlit web app that uses Google Gemini AI to help students explore personalized career paths, skill suggestions, and learning resources for the evolving job market.

## Features

- Clean, friendly single-page interface
- Submit your name, education level, interests, skills you have, skills you want to learn, and hobbies
- Instantly receive AI-powered career domains, key skills to build, project ideas, and motivational tips

## How to Run

1. Clone or download this folder (or unzip if submitted as a zip).
2. Open a terminal in this folder.
3. Install the Python dependencies: pip install -r requirements.txt
4. Get an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
5. Set your GEMINI_API_KEY environment variable:
- On Mac/Linux:
  
  export GEMINI_API_KEY="your_api_key_here"
  
- On Windows (CMD):
  
  set GEMINI_API_KEY=your_api_key_here
  
- On Windows (PowerShell):
  
  $env:GEMINI_API_KEY="your_api_key_here"
  
6. Run the app: streamlit run app.py or python -m streamlit run app.py

## Notes

- Your API key is *required* for Gemini AI features and should never be shared publicly.
- All user data remains local to your computer.
- This app is for prototype/competition/demo use.

---

Made for Gen AI Exchange Hackathon! 
by Yash Kapoor.