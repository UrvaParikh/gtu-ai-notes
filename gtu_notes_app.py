import streamlit as st
from openai import OpenAI
import html
from fpdf import FPDF
import os

# Page Config
st.set_page_config(page_title="GTU AI Notes Generator", layout="centered")

import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai"]["api_key"])
# Header
st.markdown("""
    <h2 style='text-align: center; color: #336699;'>📘 GTU AI Notes Generator</h2>
""", unsafe_allow_html=True)

# Subject Dropdown
subject = st.selectbox("📚 Select Subject:", [
    "Operating System",
    "COA",
    "Digital Fundamentals",
    "Probability & Statistics",
    "Discrete Mathematics",
    "PEM"
])

# Topic Input
topic = st.text_input("📝 Enter Topic (e.g., Paging, FSM, Boolean Algebra)")

# Generate Button
if st.button("Generate Notes"):
    if not topic:
        st.error("Please enter a topic to generate notes.")
    else:
        with st.spinner("⏳ Generating notes, please wait..."):
            try:
                # Prompt
                prompt = f"Generate short but clear GTU-style notes for the subject '{subject}' on the topic '{topic}'. Include definitions, key points, and examples where possible."

                # API Call using modern syntax
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that writes study notes for GTU students."},
                        {"role": "user", "content": prompt}
                    ]
                )

                generated_notes = response.choices[0].message.content.strip()
                safe_notes = html.escape(generated_notes)

                # Display Notes
                st.markdown(
                    f"<div style='background-color: #f9f9f9; padding: 15px; border-radius: 10px; white-space: pre-wrap;'>{safe_notes}</div>",
                    unsafe_allow_html=True
                )

                # PDF Generation
                if st.button("📄 Download Notes as PDF"):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_auto_page_break(auto=True, margin=15)
                    pdf.set_font("Arial", size=12)

                    for line in generated_notes.split('\n'):
                        pdf.multi_cell(0, 10, line)

                    pdf_filename = f"{subject}_{topic}_notes.pdf"
                    pdf.output(pdf_filename)

                    with open(pdf_filename, "rb") as f:
                        st.download_button("⬇️ Download PDF", f, file_name=pdf_filename)

            except Exception as e:
                st.error(f"❌ Error generating notes: {str(e)}")

# Footer
st.markdown("---")
st.markdown("👨‍💻 Developed by Urva Parikh | GTU Notes Assistant", unsafe_allow_html=True)
