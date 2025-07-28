import streamlit as st
import yagmail

# Streamlit UI
st.set_page_config(page_title="📧 Email Automation App")
st.title("📧 Email Automation with Streamlit")
st.markdown("Send automated emails easily with your Gmail account.")

# Input fields
sender_email = st.text_input("Your Gmail Address")
sender_password = st.text_input("App Password (Not your Gmail password)", type="password")
receiver_email = st.text_input("Recipient Email")
subject = st.text_input("Email Subject")
message = st.text_area("Email Message")

# Send button
if st.button("Send Email"):
    if not sender_email or not sender_password or not receiver_email or not message:
        st.error("All fields are required!")
    else:
        try:
            yag = yagmail.SMTP(sender_email, sender_password)
            yag.send(to=receiver_email, subject=subject, contents=message)
            st.success(f"✅ Email successfully sent to {receiver_email}")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
