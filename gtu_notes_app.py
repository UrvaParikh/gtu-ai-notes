import streamlit as st
import openai
from fpdf import FPDF

st.set_page_config(page_title="GTU AI Notes Generator", layout="centered")

st.title("📘 GTU AI Notes Generator")

subject = st.text_input("Enter subject name:")
topic = st.text_input("Enter topic name:")

final_topic = f"{subject} - {topic}" if subject and topic else topic

if st.button("Generate Notes"):
    if final_topic:
        with st.spinner("Generating..."):
            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
