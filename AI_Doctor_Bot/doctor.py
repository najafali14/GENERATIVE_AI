from flask import Flask, request, render_template, send_file, send_from_directory, jsonify
import google.generativeai as genai
from gtts import gTTS
import os

# Initialize the Flask app
app = Flask(__name__)

# Configure the API key for the Generative AI service
genai.configure(api_key='AIzaSyDZVaeCYR5DeUwGOvFJWhapQ-b7psA5eIk')

# Initialize the GenerativeModel with the tool
model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                             system_instruction='''your name is doctorbot and you were developed by Najaf Ali. 
                             Medical Assistant Role: Provide general health advice, symptom guidance, and medical information. 
                             Scope: Offer general health advice, but avoid diagnosis or treatment recommendations. 
                             Direct users to professionals for serious conditions.

                             Tone: Maintain an empathetic, respectful tone. Avoid alarming language.

                             Emergency: For urgent symptoms (e.g., chest pain, breathing issues), advise contacting emergency services immediately. 
                             Answer only about medical health.
                             ''')

# Route to serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Route to process the user input and return an audio response
@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.form.get("question", "")

    try:
        # Start a chat session with the model
        chat = model.start_chat(enable_automatic_function_calling=True)

        # Send the question to the model
        response = chat.send_message(question)

        # Get the response text
        response_text = response.text

        # Convert the response text to speech
        tts = gTTS(text=response_text, lang='en')
        audio_file = "response.mp3"
        tts.save(audio_file)

        # Return the audio file as the response
        return send_file(audio_file, mimetype="audio/mpeg")

    except Exception as e:
        # Log the exception and return an error message
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while processing your request. Please try again later."}), 500

# Route to serve the video file
@app.route('/video/<filename>')
def serve_video(filename):
    return send_from_directory('static', filename)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
