import streamlit as st
from preproc import process_and_group_chat
from analysis import generate_visualizations, generate_relationship_summary
from pdf_generator import create_pdf_report

def analyze_page():
    """Handles the analysis page logic with PDF generation."""
    st.markdown("<h1 style='text-align: center; color: #FF4E92;'>📊 Relationship Message Analysis</h1>", unsafe_allow_html=True)

    # Custom CSS for styling
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #2E004F, #7A1EA1);
                color: white;
            }

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

            .stButton>button:hover {
                background: #FF0080;
            }

            .block-container {
                max-width: 800px;
                margin: auto;
                padding-top: 50px;
            }

            .upload-container {
                text-align: center;
                padding: 20px;
                border: 2px dashed #FF4E92;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.1);
            }

            .stDownloadButton>button {
                background: #FF4E92;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                transition: 0.3s;
            }

            .stDownloadButton>button:hover {
                background: #FF0080;
            }
        </style>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("⬅️ Go Back"):
        st.session_state.page = "home"
        st.rerun()

    # **📺 Embedded YouTube Video Tutorial**
    st.markdown("<h3 style='text-align: center;'>🎥 How to Export and Upload Your WhatsApp Chat</h3>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=DilHH7EloTQ")  # ✅ Replace with your actual YouTube link

    # File uploader with custom styling
    st.markdown("<div class='upload-container'>📂 <b>Upload your chat file (.txt)</b></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["txt"])

    if uploaded_file is not None:
        chat_data = uploaded_file.read().decode("utf-8").splitlines()
        df = process_and_group_chat(chat_data)

        if 'report_data' not in st.session_state:
            st.session_state.report_data = {
                'figures': [],
                'happy_summary': '',
                'sad_summary': ''
            }

            # Generate and store visualizations
            with st.spinner("📊 Generating visualizations..."):
                figures = generate_visualizations(df, st.container(), st.container())
                st.session_state.report_data['figures'] = figures

            # Generate and store summaries
            with st.spinner("🧠 Analyzing relationship trends..."):
                happy_summary, sad_summary = generate_relationship_summary(df)
                st.session_state.report_data['happy_summary'] = happy_summary
                st.session_state.report_data['sad_summary'] = sad_summary

        # Download button
        st.markdown("<hr style='border-top: 2px solid #FF4E92;'>", unsafe_allow_html=True)
        pdf_data = create_pdf_report(
            df,
            st.session_state.report_data['happy_summary'],
            st.session_state.report_data['sad_summary'],
            st.session_state.report_data['figures']
        )
        
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_data,
            file_name="relationship_analysis.pdf",
            mime="application/pdf"
        )

    else:
        st.warning("👆 Upload a chat file to analyze messages!")

# Run the page
if __name__ == "__main__":
    analyze_page()
