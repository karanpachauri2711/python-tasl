from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from openai import OpenAI
from flask import Flask, jsonify, request, render_template_string
import traceback

app=Flask(__name__)

base_url = "https://sarkariresult.com.cm/"

# Step 1: Fetch HTML content from the URL
try:
    with urlopen(base_url, timeout=10) as response:
        html = response.read().decode('utf-8')

    # Step 2: Parse HTML content with BeautifulSoup
    mysoup = BeautifulSoup(markup=html, features="html.parser")

    # Step 3: Extract body content as plain text
    if mysoup.body:
        data = mysoup.body.get_text(strip=True, separator="\n")
    else:
        data = "No body content found"
    print("Data extracted successfully")
except (URLError, HTTPError) as e:
    print(f"Error fetching data: {e}")
    data = "Error fetching website data"
except Exception as e:
    print(f"Unexpected error: {e}")
    data = "Error fetching website data"

# Set up Gemini API key and client
gemini_api_key="AIzaSyCwgJs04uWlGYGRTQZ8EWTK1yWev0bYLdo"
client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

@app.route("/")
def home():
    return "Flask app is running! Go to /exam for exam information."

@app.route("/exam", methods=['GET', 'POST'])
def examai():
    if request.method == 'GET':
        # Return HTML form for input
        html_form = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Exam Information Assistant</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                .form-container { background: #f5f5f5; padding: 30px; border-radius: 10px; }
                input[type="text"] { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
                button { background: #007bff; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
                button:hover { background: #0056b3; }
                .result { margin-top: 20px; padding: 20px; background: white; border-radius: 5px; border-left: 4px solid #007bff; }
            </style>
        </head>
        <body>
            <div class="form-container">
                <h1>📚 Exam Information Assistant</h1>
                <p>Ask me about upcoming government exams, job opportunities, and more!</p>
                <form method="POST">
                    <input type="text" name="userprompt" placeholder="e.g., What are the latest government job opportunities?" required>
                    <button type="submit">Get Information</button>
                </form>
            </div>
        </body>
        </html>
        """
        return html_form
    
    elif request.method == 'POST':
        try:
            print("Starting examai function...")
            userprompt = request.form.get('userprompt', 'give the new sarkari result')
            print(f"User prompt: {userprompt}")
            print(f"Data length: {len(data)}")
            print(f"First 200 chars of data: {data[:200]}")
            
            # Truncate data if it's too long for API
            truncated_data = data[:8000] if len(data) > 8000 else data
            
            mymsg = [
                {"role": "system", "content": f"You are AI Assistant.assist to user for upcoming exams . Here is exam information: {truncated_data}"},
                {"role": "user", "content": userprompt}
            ]
            print("Making API call to Gemini...")
            response = client.chat.completions.create(model="gemini-2.0-flash", messages=mymsg)
            result = response.choices[0].message.content
            print("API call successful")
            
            # Return result with styling
            result_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Exam Information Assistant</title>
                <style>
                    body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
                    .form-container {{ background: #f5f5f5; padding: 30px; border-radius: 10px; }}
                    input[type="text"] {{ width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }}
                    button {{ background: #007bff; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }}
                    button:hover {{ background: #0056b3; }}
                    .result {{ margin-top: 20px; padding: 20px; background: white; border-radius: 5px; border-left: 4px solid #007bff; white-space: pre-wrap; }}
                    .back-btn {{ background: #6c757d; color: white; padding: 8px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin-top: 10px; }}
                </style>
            </head>
            <body>
                <div class="form-container">
                    <h1>📚 Exam Information Assistant</h1>
                    <p>Ask me about upcoming government exams, job opportunities, and more!</p>
                    <form method="POST">
                        <input type="text" name="userprompt" placeholder="e.g., What are the latest government job opportunities?" required>
                        <button type="submit">Get Information</button>
                    </form>
                    <div class="result">
                        <h3>🤖 AI Response:</h3>
                        <p>{result}</p>
                    </div>
                    <a href="/exam" class="back-btn">Ask Another Question</a>
                </div>
            </body>
            </html>
            """
            return result_html
            
        except Exception as e:
            print(f"Error in examai function: {e}")
            print(traceback.format_exc())
            return jsonify({"error": str(e)}), 500
#userprompt=input()
#hello = examai(userprompt)
#print(hello)
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
