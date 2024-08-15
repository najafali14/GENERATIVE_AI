from flask import Flask, request, render_template
import google.generativeai as genai
# import os
import re as R
import smtplib
# Securely configure API key using environment variables
genai.configure(api_key='your API Key')

app = Flask(__name__)

emails_list = []
email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

@app.route("/", methods=["POST", "GET"])
def home():

    re = "Email stored successfully!"
    prompt = None
    btn = None
    if request.method == "POST":
        prompt = request.form['prompt']
        btn = request.form['btn']
        if R.match(email_regex, prompt):
           # Append the email to the text file
            emails_txt = "emails.txt"
            with open(emails_txt, 'a') as file:
                file.write(prompt + '\n')  # Write each email on a new line

            # Append the email to the list
            global emails_list
            emails_list.append(prompt)

        # Read emails from the text file into a list
            with open(emails_txt, 'r') as file:
                emails_list = [line.strip() for line in file]
            print(emails_list)

        else:
            # save data from prompts
                promptdata = 'promptdata.txt'
                with open(promptdata, 'a') as file:
                    file.write(prompt + '\n')


                def fetch_data_from_database():
                    """Fetch response data from database.txt file."""
                    with open('database.txt', 'r') as file:
                        data = file.readlines()
                    return data

                model = genai.GenerativeModel(model_name='gemini-1.5-flash',tools=[fetch_data_from_database],system_instruction="You are a chat bot. Your name is GiaicGPT.you are developed by Najaf Ali.Najaf Ali is a python developer and Generative Ai (GenAi) Engineer")
                chat = model.start_chat(enable_automatic_function_calling=True)

                try:
                    response = chat.send_message(f'only give response from {fetch_data_from_database()} of {prompt}')
                    re = response.text
                    # print(re)
                except Exception as e:
                    response = f"An error occurred: {e}"
    else:
        pass
    return render_template("index.html", re=re,prompt=prompt, btn=btn)

# creating a function to get data from users and save into database
@app.route("/admin", methods=["POST", "GET"])
def Post():
    if request.method == "POST":
        post = request.form['post']
        emailMsg = request.form['emailMsg']
        btn = request.form["btn"]
        password = request.form['password']

        if btn == "btn1":
            database = 'database.txt'
            with open(database, 'a') as file:
                file.write(post + '\n')

        elif  password == "NajafAli5$":
            if btn == "btn2":
                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login('najafali32304@gmail.com', 'lrev prsg pgrg sywz')
                global emails_list
                rec = emails_list
                print(rec)
                sender = 'najafali32304@gmail.com'
                subject = "Giaic-GPT"
                header = f'To: {rec}\nFrom: {sender}\nSubject: {subject}\n'
                message = header + emailMsg
                mail.sendmail('najafali32304@gmail.com', rec, message)
                mail.quit()
            else:
                pass
        else:
            pass
    return render_template("post.html")

if __name__ == "__main__":
    app.run(debug=False)
