from flask import Flask, render_template, request
import google.generativeai as genai
import requests

app = Flask(__name__)

genai.configure(api_key='Your API Key')

def summarize_blog_url_content(url: str):
    """Summary of blog URL content"""
    try:
        response = requests.get(url)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions and return the error
        return None, f"An error occurred: {e}"

# Define the route for the chatbot interface
@app.route('/', methods=['GET', 'POST'])
def chatbot():
    summary = None
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                          tools=[summarize_blog_url_content],
                                          system_instruction="Summarize the blog content.")
            chat = model.start_chat(enable_automatic_function_calling=True)
            response = chat.send_message(url)
            summary = response.text

    return render_template('chatbot.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
