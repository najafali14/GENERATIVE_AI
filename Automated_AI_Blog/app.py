from flask import Flask,render_template
app = Flask(__name__)

import google.generativeai as genai

genai.configure(api_key=your api key)


@app.get("/")
def Home():
    # post title generation
    model = genai.GenerativeModel(model_name='gemini-1.5-flash',system_instruction='''
Generate a catchy and informative blog title on the latest advancements in AI technology,
     focusing on how it impacts daily life and industries. Keep the title between 6-10 words
     and make it engaging to attract tech enthusiasts and general readers.write only one title
                                  at a time on any topic.
''')
    chat = model.start_chat(enable_automatic_function_calling=True)
    title_response = chat.send_message("create a title on technology ")
    title = title_response.text

    # post content generation
    model1 = genai.GenerativeModel(model_name='gemini-1.5-flash',system_instruction='''
Create engaging and informative blog posts that resonate with readers 
                                   interested in technology, AI, and related fields.
''')
    chat1 = model1.start_chat(enable_automatic_function_calling=True)
    post_response = chat1.send_message(f'create post content on: {title}')
    post = post_response.text

    return render_template("index.html", title=title, post=post)
if __name__ == "__main__":
    app.run(debug=True)
