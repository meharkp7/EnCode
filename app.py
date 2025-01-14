from flask import Flask, render_template, jsonify
from main import conversation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-conversation', methods=['GET'])
def start_conversation():
    conversation()  # Start the conversation logic
    return jsonify({"message": "Conversation ended. Thank you!"})

if __name__ == '__main__':
    app.run(debug=True)
