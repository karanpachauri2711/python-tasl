import streamlit as st
import pywhatkit
import datetime

st.set_page_config(page_title="WhatsApp Message Sender", layout="centered")
st.title("📲 Send WhatsApp Message")

# Input fields
number = st.text_input("📞 Enter phone number (with country code)", value="+91")
message = st.text_area("💬 Type your message")
send_now = st.checkbox("Send Immediately (will send in 1 minute from now)")

# Manual time input (optional)
if not send_now:
    hour = st.number_input("Hour (24hr format)", min_value=0, max_value=23, value=datetime.datetime.now().hour)
    minute = st.number_input("Minute", min_value=0, max_value=59, value=(datetime.datetime.now().minute + 2) % 60)

if st.button("🚀 Send Message"):
    try:
        if send_now:
            now = datetime.datetime.now() + datetime.timedelta(minutes=1)
            pywhatkit.sendwhatmsg(number, message, now.hour, now.minute)
        else:
            pywhatkit.sendwhatmsg(number, message, hour, minute)
        st.success("✅ Message scheduled successfully! WhatsApp Web will open to send it.")
    except Exception as e:
        st.error(f"❌ Error: {e}")