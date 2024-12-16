import streamlit as st
from frontend.main_app import render_main_app
from frontend.chat_interface import render_chat_interface
from frontend.resume_ranker import render_resume_ranker
from frontend.job_recommender import render_job_recommender
from frontend.job_scraper import render_job_scraper
from frontend.about_us import render_about_us
import os
from dotenv import load_dotenv
import base64

# Set the page layout to wide for better visual presentation
st.set_page_config(layout="wide", page_title="Resume Analyzer")
st.image("resume_analyzer.jpeg", width=150)

# Load environment variables
load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Function to save and validate Google API Key
def manage_google_api_key():
    """Manage Google API Key input and validation"""
    # Always create a key input in the sidebar
    st.sidebar.header("Google API Key Setup")
    
    # Check if API key is already in session state
    if 'google_api_key' not in st.session_state:
        st.session_state['google_api_key'] = os.getenv("GOOGLE_API_KEY", "")
    
    # API Key input
    new_api_key = st.sidebar.text_input(
        "Enter your Google API Key", 
        value=st.session_state['google_api_key'],
        type="password",
        key="google_api_key_input"
    )
    
    # Save button
    if st.sidebar.button("Save API Key"):
        if new_api_key and len(new_api_key.strip()) > 10:
            # Save to session state
            st.session_state['google_api_key'] = new_api_key
            
            # Optional: Write to .env files if needed
            try:
                # Encode the API key
                encoded_key = base64.b64encode(new_api_key.encode()).decode()
                
                # Write to frontend .env
                with open(os.path.join('frontend', '.env'), 'w') as f:
                    f.write(f"GOOGLE_API_KEY={encoded_key}\n")
                
                # Write to backend .env
                with open(os.path.join('backend', '.env'), 'w') as f:
                    f.write(f"GOOGLE_API_KEY={encoded_key}\n")
                
                st.sidebar.success("API Key saved successfully!")
            except Exception as e:
                st.sidebar.error(f"Error saving API Key: {e}")
        else:
            st.sidebar.error("Please enter a valid API Key")
    
    # Return the API key
    return st.session_state['google_api_key']

# Function to handle admin login
def admin_login():
    """Admin login page"""
    st.title("Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state["admin_logged_in"] = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password. Please try again.")

def main():
    # Get Google API Key
    google_api_key = manage_google_api_key()
    
    # Validate API Key
    if not google_api_key or len(google_api_key.strip()) <= 10:
        st.warning("Please enter a valid Google API Key in the sidebar to proceed.")
        return

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ("Resume Screener", "Resume Ranker (Admin)", "Job Recommender", "Job Scraper", "About Us")
    )

    if not st.session_state["admin_logged_in"]:
        if page == "Resume Ranker (Admin)":
            admin_login()
            return  
    else:
        if page == "Resume Ranker (Admin)":
            st.title("Admin Panel - Resume Ranker")
            render_resume_ranker()

    # Page Routing
    if page == "Resume Screener":
        st.title("Resume Screener")
        col1, col2 = st.columns([3, 2])
        with col1:
            render_main_app()
        with col2:
            render_chat_interface()
    
    elif page == "Job Recommender":
        render_job_recommender()

    elif page == "Job Scraper":
        render_job_scraper()
    
    elif page == "About Us":
        render_about_us()

# Initialize session state for admin login if not already set
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# Script execution through the 'main' function
if __name__ == "__main__":
    main()
