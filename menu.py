import streamlit as st
import tweepy
import requests
from instagrapi import Client
import pywhatkit as kit
import yagmail
import datetime

st.set_page_config(page_title="📢 Social Automation App")
st.title("📢 Social Media & Messaging Automation")

platform = st.sidebar.selectbox("Choose Platform", [
    "Twitter", "Instagram", "Facebook Page", "LinkedIn", "WhatsApp", "Email"])

# --- Twitter ---
if platform == "Twitter":
    st.subheader("🐦 Post to Twitter")
    api_key = st.text_input("API Key")
    api_secret = st.text_input("API Secret", type="password")
    access_token = st.text_input("Access Token")
    access_secret = st.text_input("Access Token Secret", type="password")
    tweet = st.text_area("Tweet Content", max_chars=280)

    if st.button("Post to Twitter"):
        try:
            auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
            api = tweepy.API(auth)
            api.update_status(status=tweet)
            st.success("✅ Tweet posted!")
        except Exception as e:
            st.error(f"❌ {e}")

# --- Instagram ---
elif platform == "Instagram":
    st.subheader("📸 Post to Instagram")
    username = st.text_input("Instagram Username")
    password = st.text_input("Instagram Password", type="password")
    photo = st.file_uploader("Upload Image", type=['jpg', 'png'])
    caption = st.text_area("Caption")

    if st.button("Post to Instagram") and photo:
        try:
            with open("temp.jpg", "wb") as f:
                f.write(photo.read())
            cl = Client()
            cl.login(username, password)
            cl.photo_upload("temp.jpg", caption=caption)
            st.success("✅ Posted to Instagram!")
        except Exception as e:
            st.error(f"❌ {e}")

# --- Facebook ---
elif platform == "Facebook Page":
    st.subheader("📘 Post to Facebook Page")
    page_id = st.text_input("Page ID")
    access_token = st.text_input("Page Access Token", type="password")
    message = st.text_area("Post Content")

    if st.button("Post to Facebook"):
        try:
            url = f'https://graph.facebook.com/{page_id}/feed'
            payload = {'message': message, 'access_token': access_token}
            res = requests.post(url, data=payload)
            st.success(f"✅ Facebook Post Result: {res.json()}")
        except Exception as e:
            st.error(f"❌ {e}")

# --- LinkedIn ---
elif platform == "LinkedIn":
    st.subheader("🔗 Post to LinkedIn")
    access_token = st.text_input("LinkedIn Access Token", type="password")
    person_urn = st.text_input("Your LinkedIn Person URN")
    message = st.text_area("Post Content")

    if st.button("Post to LinkedIn"):
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            payload = {
                "author": person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": message},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
            }
            res = requests.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, json=payload)
            st.success(f"✅ LinkedIn Post Result: {res.json()}")
        except Exception as e:
            st.error(f"❌ {e}")

# --- WhatsApp ---
elif platform == "WhatsApp":
    st.subheader("📲 Schedule WhatsApp Message")
    number = st.text_input("Recipient Number (with country code)")
    message = st.text_area("Message")
    now = datetime.datetime.now()
    hour = st.number_input("Hour (24hr format)", 0, 23, value=(now.hour + 1) % 24)
    minute = st.number_input("Minute", 0, 59, value=(now.minute + 2) % 60)

    if st.button("Send WhatsApp"):
        try:
            kit.sendwhatmsg(number, message, int(hour), int(minute))
            st.success("✅ Message scheduled!")
        except Exception as e:
            st.error(f"❌ {e}")

# --- Email ---
elif platform == "Email":
    st.subheader("✉️ Send Email")
    sender = st.text_input("Your Gmail")
    app_password = st.text_input("App Password", type="password")
    receiver = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    body = st.text_area("Message Body")

    if st.button("Send Email"):
        try:
            yag = yagmail.SMTP(sender, app_password)
            yag.send(to=receiver, subject=subject, contents=body)
            st.success("✅ Email sent!")
        except Exception as e:
            st.error(f"❌ {e}")