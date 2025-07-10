import streamlit as st
from datetime import datetime

st.set_page_config(page_title="OfficeGenie - Helpdesk Form", page_icon="🧞", layout="centered")

st.title("🧞 OfficeGenie – Smart Workplace Helpdesk")
st.markdown("Submit your workplace query below. Our AI assistant will handle it!")

with st.form("query_form"):
    full_name = st.text_input("Full Name", placeholder="e.g. Ananya Sharma")
    email = st.text_input("Email", placeholder="e.g. ananya@company.com")
    department = st.selectbox("Department", ["", "IT", "HR", "Finance", "Admin", "Engineering", "Legal", "Operations"])
    message = st.text_area("Message / Request", placeholder="Describe your issue or request here...", height=150)
    submitted = st.form_submit_button("Submit Request")

if submitted:
    if not full_name or not email or not message:
        st.error("Please fill in all required fields.")
    else:
        # Collect structured input
        user_input = {
            "full_name": full_name,
            "email": email,
            "department": department,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }

        # Display input summary (for now)
        st.success("Your request has been received!")
        st.json(user_input)

        # Here you can pass `user_input` to your LLM pipeline next
