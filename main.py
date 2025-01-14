#TRY 1 TO COMPLETE POORA CONVERSATION    

from flask import Flask, render_template, request, jsonify
import spacy

# Initialize the Flask app
app = Flask(__name__)

# Load the language model
nlp = spacy.load("en_core_web_sm")

# Define intents and responses
intents = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening", "hey there"],
    "product_inquiry": ["tell me about your product", "what do you sell", "give me more info about your products"],
    "price_inquiry": ["how much does it cost", "what is the price", "pricing details", "how much is it"],
    "thank_you": ["thank you", "thanks", "appreciate it"],
    "goodbye": ["bye", "goodbye", "see you", "later", "talk to you soon"],
    "default": ["sorry", "what", "huh", "can you repeat that"]
}

responses = {
    "greeting": "Hello! How can I assist you with your purchase today?",
    "product_inquiry": "We offer a variety of products. Which category interests you?",
    "price_inquiry": "Our products range from $10 to $500 depending on the item. What product are you interested in?",
    "thank_you": "You're welcome! I'm here to help.",
    "goodbye": "Goodbye! Have a great day!",
    "default": "I'm sorry, I didn't quite catch that. Could you please repeat?"
}

# Function to match intent
def match_intent(text):
    text = text.lower()
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in text:
                return intent
    return "default"

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle conversation
@app.route('/conversation', methods=['POST'])
def conversation():
    user_input = request.json.get("text", "")
    intent = match_intent(user_input)
    response = responses.get(intent, responses["default"])
    return jsonify({"response": response})

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
