# instagram_post_app.py
import streamlit as st
from instagrapi import Client
import os

st.title("Instagram Image Poster (Personal Account)")

username = st.text_input("Instagram Username")
password = st.text_input("Instagram Password", type="password")
caption = st.text_area("Post Caption")
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if st.button("Post to Instagram"):
    if username and password and uploaded_file:
        try:
            # Save image locally
            img_path = os.path.join("temp.jpg")
            with open(img_path, "wb") as f:
                f.write(uploaded_file.read())

            # Login and post
            cl = Client()
            cl.login(username, password)
            cl.photo_upload(img_path, caption)

            st.success("Posted to Instagram successfully!")
            os.remove(img_path)
        except Exception as e:
            st.error(f"Failed: {e}")
    else:
        st.warning("Please fill all fields.")