import streamlit as st
from analyze import analyze_page

# App Configuration
st.set_page_config(page_title="❤️ Relationship Analyzer", layout="wide")

# Custom Styles - Match the app to the banner design
st.markdown("""
    <style>
        /* Background color for the entire app */
        .stApp {
            background: linear-gradient(135deg, #2E004F, #7A1EA1);
            color: white;
        }
        
        /* Text Colors */
        h1, h2, h3, h4, h5, h6 {
            color: #FF4E92;
        }

        /* Buttons */
        .stButton>button {
            background: linear-gradient(90deg, #FF4E92, #FF0080);
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 18px;
            transition: 0.3s;
        }
        
        /* Hover effect */
        .stButton>button:hover {
            background: #FF0080;
        }

        /* Center content */
        .block-container {
            max-width: 800px;
            margin: auto;
            padding-top: 50px;
        }

        /* Hide sidebar */
        section[data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Main App Layout (No Sidebar)
if st.session_state.page == "home":
    st.image("home_banner.png", use_container_width=True)
    st.title("Welcome to the Relationship Message Analyzer ❤️")
    st.write("Upload your chat file and get deep insights into your conversations!")

    if st.button("Start Analysis 🚀"):
        st.session_state.page = "analyze"
        st.rerun()  # Refresh the app to go to analyze

elif st.session_state.page == "analyze":
    analyze_page()


