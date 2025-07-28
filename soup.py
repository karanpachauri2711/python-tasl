import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from flask import Flask

app=Flask(__name__)

base_url = "https://sarkariresult.com.cm/"

# Step 1: Fetch HTML content from the URL
response = requests.get(base_url)
html = response.text

# Step 2: Parse HTML content with BeautifulSoup
mysoup = BeautifulSoup(markup=html, features="html.parser")

# Step 3: Extract body content as plain text
data = mysoup.body.get_text(strip=True, separator="\n")
print(data)

# Set up Gemini API key and client
gemini_api_key="AIzaSyCwgJs04uWlGYGRTQZ8EWTK1yWev0bYLdo"
client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

@app.route("/exam")
userprompt="give the new sarkari result"
def examai(userprompt):
    mymsg = [ {"role": "system", "content": f"You are AI Assistant.assist to user for upcoming exams . Here is exam information: {data}"},{"role": "user", "content": userprompt}]
    response = client.chat.completions.create(model="gemini-2.0-flash",messages=mymsg)
    result = response.choices[0].message.content
    return result
#userprompt=input()
#hello = examai(userprompt)
#print(hello)
app.run()
