import streamlit as st
import plotly.express as px
import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords
from openai_api import analyze_weeks    
import emoji

#import Emojis
def extract_emojis(text):
    return [char for char in text if char in emoji.EMOJI_DATA]
# Download stopwords
nltk.download("stopwords")
stop_words = set(stopwords.words("portuguese"))

def generate_visualizations(df, col1, col2):
    """Generate modernized graphs with better UI integration."""
    figures = []

    # Apply custom style
    st.markdown("""
        <style>
            .graph-card {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    #################################### Messages Per Person
    msg_count = df["Sender"].value_counts().reset_index()
    msg_count.columns = ["Sender", "Messages"]

    fig1 = px.bar(
        msg_count, x="Sender", y="Messages", text="Messages", color="Sender",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig1.update_traces(textposition="outside", marker=dict(line=dict(width=1, color="black")))
    fig1.update_layout(
        title="Messages Sent by Each Person",title_font=dict(size=20, color="hotpink"), 
        xaxis_title="User",
        yaxis_title="Message Count",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=False
    )

    with col1:
        st.markdown('<div class="graph-card">', unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    figures.append(fig1)

    ############################# Activity By Hour
    df["Hour"] = df["Datetime"].dt.hour
    hourly_activity = df.groupby(["Sender", "Hour"]).size().reset_index(name="Count")

    fig2 = px.line(
        hourly_activity, x="Hour", y="Count", color="Sender",
        markers=True, color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig2.update_traces(line=dict(width=3), marker=dict(size=8, opacity=0.8))
    fig2.update_layout(
        title="Activity by Hour",title_font=dict(size=20, color="hotpink"),
        xaxis_title="Hour of the Day",
        yaxis_title="Messages Sent",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    with col2:
        st.markdown('<div class="graph-card">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    figures.append(fig2)

    ################################## Average Response Time
    df["Response_Time"] = df["Datetime"].diff().dt.total_seconds()

    # Remove inactive periods (greater than 6 hours)
    df.loc[df["Response_Time"] > 21600, "Response_Time"] = None

    # Convert to minutes
    response_times = df.groupby("Sender")["Response_Time"].mean().dropna().reset_index()
    response_times["Response_Time"] = (response_times["Response_Time"] / 60).astype(int)

    fig3 = px.bar(
        response_times, x="Sender", y="Response_Time", text="Response_Time", color="Sender",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig3.update_layout(
        title="Average Response Time (Minutes)",title_font=dict(size=20, color="hotpink"),
        xaxis_title="User",
        yaxis_title="Response Time (min)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    with col1:
        st.markdown('<div class="graph-card">', unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    figures.append(fig3)



# 📊 Top 5 Emojis (Overall)
    df["Emojis"] = df["Message"].apply(extract_emojis)
    all_emojis = [e for sublist in df["Emojis"] for e in sublist]
    top_5_emojis = Counter(all_emojis).most_common(5)

    if top_5_emojis:
        emoji_text = " ".join(f"{e[0]} ({e[1]})" for e in top_5_emojis)
        st.subheader("🔥 Top 5 Emojis Used")
        st.write(emoji_text)




    ################################## Top 10 Words (Without 1-character words)
    def remove_stopwords(text):
        words = text.split()
        return " ".join([word for word in words if word not in stop_words and len(word) > 1])

    df["Processed_Message_NoStopwords"] = df["Processed_Message"].apply(remove_stopwords)
    
    words_per_person = {
        sender: Counter(" ".join(df[df["Sender"] == sender]["Processed_Message_NoStopwords"]).split()) 
        for sender in df["Sender"].unique()
    }

    word_data = [
        {"Sender": sender, "Word": word, "Count": count}
        for sender, words in words_per_person.items()
        for word, count in words.most_common(10)
    ]

    word_df = pd.DataFrame(word_data)

    fig4 = px.bar(
        word_df, x="Word", y="Count", color="Sender", barmode="group",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig4.update_layout(
        title="Top 10 Words Used",title_font=dict(size=20, color="hotpink"),
        xaxis_title="Word",
        yaxis_title="Count",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    with col2:
        st.markdown('<div class="graph-card">', unsafe_allow_html=True)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    figures.append(fig4)



    # Sentiment Analysis Over Time (Smooth Curves)
    df["Week"] = df["Datetime"].dt.to_period("W").astype(str)
    sentiment_weekly = df.groupby("Week")["Sentiment"].mean().reset_index()

    fig5 = px.area(
        sentiment_weekly, x="Week", y="Sentiment", 
        markers=True, color_discrete_sequence=["#FF5733"]
    )
    fig5.update_traces(line=dict(width=3), marker=dict(size=10, opacity=0.8))
    fig5.update_layout(
        title="Sentiment Analysis Over Time",title_font=dict(size=20, color="hotpink"),
        xaxis_title="Week",
        yaxis_title="Average Sentiment Score",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.subheader("📈 Sentiment Analysis Over Time")
    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    figures.append(fig5)
    return figures


def generate_relationship_summary(df):
    """Uses OpenAI to generate two different relationship summaries."""
    
    # Find happiest & saddest weeks based on sentiment
    df["Week"] = df["Datetime"].dt.to_period("W").astype(str)
    sentiment_weekly = df.groupby("Week")["Sentiment"].mean().reset_index()

    max_week = sentiment_weekly.loc[sentiment_weekly["Sentiment"].idxmax()]
    min_week = sentiment_weekly.loc[sentiment_weekly["Sentiment"].idxmin()]

    happiest_week = max_week["Week"]
    saddest_week = min_week["Week"]

    happy_msgs = df[df["Week"] == happiest_week]["Message"].tolist()
    sad_msgs = df[df["Week"] == saddest_week]["Message"].tolist()

    # 🔥 Get AI-generated summaries
    happy_summary, sad_summary = analyze_weeks(
        happy_msgs, sad_msgs, happiest_week, saddest_week, 
        max_week["Sentiment"], min_week["Sentiment"]
    )

    # 🏆 Display Results
    st.markdown("<h2 style='text-align: center; color: #32CD32;'> The Happiest Week</h2>", unsafe_allow_html=True)
    st.write(happy_summary)

    st.markdown("<h2 style='text-align: center; color: #FF4500;'> The Toughest Week</h2>", unsafe_allow_html=True)
    st.write(sad_summary)

    return happy_summary, sad_summary
