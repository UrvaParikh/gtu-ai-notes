import streamlit as st
import openai
from fpdf import FPDF
import os

st.set_page_config(page_title="GTU AI Notes", layout="wide", page_icon="📘")
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>📘 GTU AI Notes Generator</h1>
    <h4 style='text-align: center; color: gray;'>Powered by OpenAI • For GTU B.Tech CSE Students</h4>
    <hr>
""", unsafe_allow_html=True)

# Your OpenAI API key
import openai
openai.api_key = "your_openai_key"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain deadlock in OS."}
    ]
)

st.markdown("### 🎯 Choose a topic or enter your own:")


topics = [
    "Deadlock in Operating System",
    "Paging vs Segmentation",
    "Normalization in DBMS",
    "TCP vs UDP",
    "Greedy Algorithm",
    "DFS vs BFS",
    "Bayes Theorem",
    "Regression in ML",
    "CPU Scheduling Algorithms",
    "Multithreading",
    "MapReduce in Big Data",
    "Naive Bayes Classifier",
    "K-means Clustering"
]

topic = st.selectbox("Choose a GTU topic:", options=topics)
custom_topic = st.text_input("Or type your own topic:")
final_topic = custom_topic if custom_topic else topic
generated_notes = ""

if st.button("Generate Notes"):
    if final_topic:
        with st.spinner("Generating..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professor who explains GTU topics in short simple notes."},
                    {"role": "user", "content": f"Explain the topic '{final_topic}' in short notes format for GTU B.Tech CSE students."}
                ]
            )
            generated_notes = response.choices[0].message.content
            st.success("✅ Notes Generated!")

            st.markdown("### 📄 Generated Notes:")
            st.markdown(
                f"<div style='background-color: #f9f9f9; padding: 15px; border-radius: 10px;'>{generated_notes}</div>",
                unsafe_allow_html=True
            )

            st.download_button(
                "📥 Download as PDF",
                data=generated_notes,
                file_name=f"{final_topic}_notes.pdf"
            )
    else:
        st.warning("Please enter or select a topic.")