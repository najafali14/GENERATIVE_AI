from flask import Flask, render_template
import time
app = Flask(__name__)
import google.generativeai as genai
genai.configure(api_key='YOUR API KEY')
model = genai.GenerativeModel(model_name='gemini-1.5-flash',system_instruction='''
Contextual Understanding: Create two-line poetic birthday quotes for Yamman, whose birthday is on September 27, emphasizing friendship with Najaf Ali.

Tone: The quotes should have a sincere, lovely, happy, warm, and masculine tone.

Personal Touch: Incorporate qualities of Yamman and the bond of friendship with Najaf.

Format: Deliver a single, short poetic quote consisting of two lines. The quotes should be impactful and memorable.

Creativity: Use rhyme, metaphor, and imagery to evoke feelings of closeness and celebration.

Frequency: Provide only one quote at a time.
''')
chat = model.start_chat(enable_automatic_function_calling=True)
response = chat.send_message("write quote for yamman birthday")
quote = response.text
# remaining days
from datetime import datetime
today = datetime(2024, 9, 24)

target_date = datetime(2024, 9, 27)

remaining_days = (target_date - today).days

@app.route('/')
def home():
    
    return render_template("index.html",quote=quote,remaining_days=remaining_days)
if __name__ == '__main__':
    app.run()
