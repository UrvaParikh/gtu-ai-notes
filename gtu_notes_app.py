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
            from fpdf import FPDF
from io import BytesIO

st.success("✅ Notes Generated!")

st.markdown("### 📄 Generated Notes:")
st.markdown(
    f"<div style='background-color: #f9f9f9; padding: 15px; border-radius: 10px;'>{generated_notes}</div>",
    unsafe_allow_html=True
)

# ✅ PDF Generation Code
pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=12)

for line in generated_notes.split('\n'):
    pdf.multi_cell(0, 10, line)

pdf_output = BytesIO()
pdf.output(pdf_output)
pdf_output.seek(0)

st.download_button(
    label="📥 Download Notes as PDF",
    data=pdf_output,
    file_name=f"{final_topic}_GTU_notes.pdf",
    mime='application/pdf'
)
