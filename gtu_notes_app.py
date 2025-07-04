import streamlit as st
import openai
import html
from fpdf import FPDF

# Set page config
st.set_page_config(page_title="GTU AI Notes Generator", layout="centered")

# App Header
st.markdown("""
    <h2 style='text-align: center; color: #336699;'>📘 GTU AI Notes Generator</h2>
""", unsafe_allow_html=True)

# OpenAI API Key (You should replace this with environment variable in real use)
openai.api_key = "YOUR_OPENAI_API_KEY"

# Subject and Topic Inputs
subject = st.selectbox("📚 Select Subject:", ["Operating System", "COA", "Digital Fundamentals", "Probability & Stats", "DM", "PEM"])
topic = st.text_input("📝 Enter Topic (e.g., Paging, FSM, Boolean Algebra)")

# Generate Notes Button
if st.button("Generate Notes"):
    if not topic:
        st.error("Please enter a topic to generate notes.")
    else:
        with st.spinner("Generating notes..."):
            try:
                # OpenAI call
                prompt = f"Generate GTU-level notes for the subject {subject} on the topic: {topic}. Include examples and definitions."
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that writes academic notes."},
                        {"role": "user", "content": prompt}
                    ]
                )
                generated_notes = response['choices'][0]['message']['content']
                safe_notes = html.escape(generated_notes)

                # Display nicely
                st.markdown(
                    f"<div style='background-color: #f9f9f9; padding: 15px; border-radius: 10px; white-space: pre-wrap;'>{safe_notes}</div>",
                    unsafe_allow_html=True
                )

                # PDF Download Option
                if st.button("📄 Download as PDF"):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_auto_page_break(auto=True, margin=15)
                    pdf.set_font("Arial", size=12)
                    for line in generated_notes.split('\n'):
                        pdf.multi_cell(0, 10, line)
                    pdf_path = f"{subject}_{topic}_notes.pdf"
                    pdf.output(pdf_path)

                    with open(pdf_path, "rb") as f:
                        st.download_button("⬇️ Click here to download PDF", f, file_name=pdf_path)

            except Exception as e:
                st.error(f"❌ Error generating notes: {e}")

# Footer
st.markdown("---")
st.markdown("👨‍💻 Developed by Urva Parikh | AI Notes for GTU Students", unsafe_allow_html=True)
