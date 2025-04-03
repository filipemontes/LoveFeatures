import openai
import os
import streamlit as st
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("Error: OpenAI API key not found. Set 'OPENAI_API_KEY'.")

client = openai.OpenAI(api_key=openai_api_key)

def generate_summary(prompt):
    """Generic function to send a prompt to OpenAI and return the result."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return response.choices[0].message.content

def analyze_weeks(happy_msgs, sad_msgs, happy_week, sad_week, happy_sentiment, sad_sentiment):
    """Generates separate summaries for the happiest and saddest weeks."""

    # Prompt for the happiest week
    happy_prompt = f"""
    **💖 The Happiest Week ({happy_week})**  
    Sentiment Score: {happy_sentiment:.2f}  

    Messages: {' '.join(happy_msgs)}

    **Task:**  
    - Describe what made this week so special (love, fun, meaningful moments).  
    - Highlight any minor negative aspects (if any) to add balance.  
       in one paragrpah
    """
    happy_summary = generate_summary(happy_prompt)

    # Prompt for the saddest week
    sad_prompt = f"""
    **💔 The Toughest Week ({sad_week})**  
    Sentiment Score: {sad_sentiment:.2f}  

    Messages: {' '.join(sad_msgs)}

    **Task:**  
    - Describe what made this week difficult (arguments, distance, stress).  
    - Mention any bright spots that helped lighten the mood.  
    in one paragrpah
    """
    sad_summary = generate_summary(sad_prompt)

    return happy_summary, sad_summary
