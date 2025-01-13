import speech_recognition as sr
import pyttsx3
import spacy
import datetime
import requests
from transformers import pipeline
import json

# Initialize speech recognition, TTS, NLU, and sentiment analysis
r = sr.Recognizer()
nlp = spacy.load("en_core_web_sm")
engine = pyttsx3.init()
sentiment_analysis = pipeline("sentiment-analysis")

# Define some simple intents and responses
intents = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening", "hey there"],
    "product_inquiry": ["tell me about your product", "what do you sell", "give me more info about your products"],
    "price_inquiry": ["how much does it cost", "what is the price", "pricing details", "how much is it"],
    "thank_you": ["thank you", "thanks", "appreciate it"],
    "goodbye": ["bye", "goodbye", "see you", "later", "talk to you soon"],
    "cart_action": ["add to cart", "put in my cart", "add this to my cart"],
    "checkout": ["checkout", "buy now", "complete purchase"],
    "default": ["sorry", "what", "huh", "can you repeat that"]
}

responses = {
    "greeting": "Hello! How can I assist you with your purchase today?",
    "product_inquiry": "We offer a variety of products, including electronics, home appliances, and accessories. Which category interests you?",
    "price_inquiry": "Our products range from $10 to $500 depending on the item. What product are you interested in?",
    "thank_you": "You're welcome! I'm here to help.",
    "goodbye": "Goodbye! Have a great day, and thank you for your interest in our products!",
    "cart_action": "The product has been added to your cart. Would you like to continue shopping?",
    "checkout": "You're about to checkout. Please confirm your details, and I'll complete the purchase.",
    "default": "I'm sorry, I didn't quite catch that. Could you please repeat?"
}

# In-memory user session data to track product preferences, context, etc.
user_sessions = {}

# Function to recognize speech and return text
def record_text(user_id):
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.3)
                audio2 = r.listen(source2, timeout=5, phrase_time_limit=10)
                MyText = r.recognize_google(audio2)
                return MyText
        except sr.RequestError as e:
            print(f"Request error: {e}")
        except sr.UnknownValueError:
            print("Unknown error occurred")

# Function to process natural language understanding (NLU) and extract useful information
def process_nlu(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    verbs = [token.text for token in doc if token.pos_ == "VERB"]
    return entities, verbs

# Function to analyze sentiment of user input (positive/negative)
def analyze_sentiment(text):
    sentiment = sentiment_analysis(text)
    return sentiment[0]['label'].lower()

# Function to match intents based on keywords in the text
def match_intent(text):
    text = text.lower()
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in text:
                return intent
    return "default"

# Function to generate response based on intent and sentiment
def respond(intent, sentiment, user_id):
    response = responses.get(intent, responses["default"])
    # Adjust tone based on sentiment
    if sentiment == "positive":
        response = "I'm glad to hear that! " + response
    elif sentiment == "negative":
        response = "I'm sorry to hear that. " + response
    return response

# Function to handle dynamic product API fetching (example)
def get_product_info():
    # Example API call to fetch product details (mock API endpoint)
    response = requests.get("https://api.example.com/products")
    if response.status_code == 200:
        products = json.loads(response.text)
        return products
    else:
        return []

# Function to provide product suggestions
def suggest_products(product_type):
    # Example: Based on the user query, fetch product suggestions
    products = get_product_info()
    suggestions = [product['name'] for product in products if product_type.lower() in product['category'].lower()]
    return suggestions

# Function to speak the response using TTS
def speak_response(response):
    engine.say(response)
    engine.runAndWait()

# Function to remember and track user preferences and actions
def update_user_session(user_id, action, data):
    if user_id not in user_sessions:
        user_sessions[user_id] = {}
    user_sessions[user_id][action] = data

# Function to handle the entire conversation flow
def conversation():
    print("Agent is ready to speak.")
    user_id = "user1"  # This can be dynamically assigned based on the system context
    while True:
        # Step 1: Record customer's speech
        text = record_text(user_id)
        print(f"Customer said: {text}")
        
        # Step 2: Process the text (NLU)
        entities, verbs = process_nlu(text)
        print(f"Entities: {entities}, Verbs: {verbs}")
        
        # Step 3: Analyze sentiment
        sentiment = analyze_sentiment(text)
        print(f"Sentiment: {sentiment}")
        
        # Step 4: Match intent based on the text
        intent = match_intent(text)
        print(f"Matched intent: {intent}")
        
        # Step 5: Respond based on intent and sentiment
        response = respond(intent, sentiment, user_id)
        print(f"Agent responds: {response}")
        
        # Step 6: If product inquiry, provide suggestions (mockup)
        if intent == "product_inquiry":
            suggestions = suggest_products("electronics")  # Example: Fetch electronics-related products
            if suggestions:
                response += " I recommend the following products: " + ", ".join(suggestions)
            else:
                response += " Unfortunately, I couldn't find any related products."
        
        # Step 7: Speak the response
        speak_response(response)
        
        # Step 8: Update user session with the current conversation
        update_user_session(user_id, "last_action", intent)
        
        # Step 9: End conversation if intent is goodbye
        if intent == "goodbye":
            break

# Start the conversation
conversation()
