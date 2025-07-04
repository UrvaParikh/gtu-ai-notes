import streamlit as st
import openai
from fpdf import FPDF

st.set_page_config(page_title="GTU AI Notes Generator", layout="centered")

st.title("📘 GTU AI Notes Generator")

st.image("https://i.imgur.com/6Fz1FjW.png", width=150)  # or upload your own logo
st.markdown("### Built by **Urva Parikh** · B.Tech CSE · AI/ML")
st.markdown("---")

# Subject Dropdown
subject = st.selectbox("📚 Select Subject", [
    "Operating System",
    "Computer Networks",
    "Database Management System",
    "Design and Analysis of Algorithms",
    "Python for Data Science",
    "Artificial Intelligence",
    "Machine Learning"
])

# Topic Dropdown (linked with subject manually for now)
topics = {
    "Operating System": ["Deadlock", "Process Scheduling", "Memory Management", "Semaphore"],
    "Computer Networks": ["OSI Model", "TCP/IP", "IP Addressing", "Routing Algorithms"],
    "Database Management System": ["Normalization", "SQL", "ER Diagrams", "Transactions"],
    "Design and Analysis of Algorithms": ["Greedy Algorithm", "Divide and Conquer", "Dynamic Programming", "Backtracking"],
    "Python for Data Science": ["NumPy", "Pandas", "Matplotlib", "Data Preprocessing"],
    "Artificial Intelligence": ["Search Algorithms", "Knowledge Representation", "Planning", "Expert Systems"],
    "Machine Learning": ["Supervised vs Unsupervised", "Regression", "Classification", "Overfitting"]
}

topic = st.selectbox("📝 Select Topic", topics[subject])

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

import yagmail

st.markdown("### 📧 Send Notes to Your Email")
user_email = st.text_input("Enter your email to receive notes as PDF:")

if st.button("📤 Send to Email"):
    if user_email:
        sender = st.secrets["EMAIL_SENDER"]
        password = st.secrets["EMAIL_PASSWORD"]
        
        yag = yagmail.SMTP(user=sender, password=password)
        yag.send(
            to=user_email,
            subject=f"{final_topic} - GTU AI Notes",
            contents="Attached are your GTU AI-generated notes.",
            attachments=pdf_output
        )
        st.success(f"✅ Notes sent to {user_email} successfully!")
    else:
        st.warning("Please enter a valid email address.")
        
import pandas as pd
import datetime

st.markdown("---")
st.subheader("📋 Feedback / Rating")

rating = st.slider("How helpful were these notes?", 1, 5, 3)
comment = st.text_input("Any suggestions or feedback? (Optional)")

if st.button("Submit Feedback"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    feedback_data = {
        "Timestamp": timestamp,
        "Subject": subject,
        "Topic": topic,
        "Rating": rating,
        "Comment": comment
    }

    df = pd.DataFrame([feedback_data])
    with open("feedback.csv", "a") as f:
        df.to_csv(f, header=f.tell()==0, index=False)

    st.success("✅ Thanks for your feedback!")
