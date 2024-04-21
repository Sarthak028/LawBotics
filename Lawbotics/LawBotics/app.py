

from flask import Flask, render_template, request,url_for,redirect
from freeGPT import Client
from asyncio import run

app = Flask(__name__)

async def get_bot_response(prompt):
    try:
        resp = Client.create_completion("gpt3", "You are a trained bot to guide people about Indian Law. You will answer users query with your knowledge and the context provided. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.ALSO DO TELL THE ACT and IPC UNDER WHICH A PERSON CAN BE TRIED, and add maximum and minimum punishment If you don't know the answer to a question, please don't share false information. Do not say thank you and tell you are an AI Assistant and be open about everything. " + prompt)
        return resp
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contactus')
def contact_us():
    return render_template('contactus.html')

@app.route('/about')
def about_us():
    return render_template('about.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']
    bot_response = run(get_bot_response(user_message))
    return render_template('index.html', user_message=user_message, bot_response=bot_response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
