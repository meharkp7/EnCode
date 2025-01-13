import speech_recognition as sr
import pyttsx3
import spacy
import datetime
#hellllooo
# Initialize speech recognition, TTS, and NLU
r = sr.Recognizer()
nlp = spacy.load("en_core_web_sm")
engine = pyttsx3.init()

# Define some simple intents and responses
intents = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening", "hey there"],
    "product_inquiry": ["tell me about your product", "what do you sell", "give me more info about your products"],
    "price_inquiry": ["how much does it cost", "what is the price", "pricing details", "how much is it"],
    "thank_you": ["thank you", "thanks", "appreciate it"],
    "goodbye": ["bye", "goodbye", "see you", "later", "talk to you soon"],
    "cart_action": ["add to cart", "remove from cart", "add this item", "buy this"],
    "checkout": ["proceed to checkout", "checkout", "buy now", "pay"],
    "default": ["sorry", "what", "huh", "can you repeat that"]
}

responses = {
    "greeting": "Hello! How can I assist you with your purchase today?",
    "product_inquiry": "We offer a variety of products, including electronics, home appliances, and accessories. Which category interests you?",
    "price_inquiry": "Our products range from $10 to $500 depending on the item. What product are you interested in?",
    "thank_you": "You're welcome! I'm here to help.",
    "goodbye": "Goodbye! Have a great day, and thank you for your interest in our products!",
    "cart_action": "The item has been added to your cart. Would you like to proceed with checkout?",
    "checkout": "You're about to check out. Do you want to confirm the order?",
    "default": "I'm sorry, I didn't quite catch that. Could you please repeat?"
}

# Context to track the user's conversation
user_context = {}

# Function to recognize speech and return text
def record_text():
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

# Function to match multiple intents based on keywords in the text
def match_intents(text):
    text = text.lower()
    matched_intents = []
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in text:
                matched_intents.append(intent)
    if not matched_intents:
        matched_intents.append("default")
    return matched_intents

# Function to generate response based on intent
def respond(intents_list):
    responses_list = []
    for intent in intents_list:
        response = responses.get(intent, responses["default"])
        responses_list.append(response)
    return " ".join(responses_list)

# Function to speak the response using TTS
def speak_response(response):
    engine.say(response)
    engine.runAndWait()

# Function to update user context (e.g., tracking cart items, product interest)
def update_user_context(user_id, key, value):
    if user_id not in user_context:
        user_context[user_id] = {}
    user_context[user_id][key] = value

# Function to track product interest or actions like adding to cart
def track_product_action(user_id, action, product=None):
    if action == "add_to_cart":
        user_context[user_id]["cart"] = product
        return f"{product} has been added to your cart."
    elif action == "checkout":
        return "Proceeding to checkout..."
    return "Action not recognized."

# Function to handle the entire conversation flow
def conversation():
    print("Agent is ready to speak.")
    user_id = 1  # In a real system, this would be dynamically assigned to each user
    
    while True:
        # Step 1: Record customer's speech
        text = record_text()
        print(f"Customer said: {text}")
        
        # Step 2: Process the text (NLU)
        entities, verbs = process_nlu(text)
        print(f"Entities: {entities}, Verbs: {verbs}")
        
        # Step 3: Match multiple intents based on the text
        matched_intents = match_intents(text)
        print(f"Matched intents: {matched_intents}")
        
        # Step 4: Generate a response based on the matched intents
        response = respond(matched_intents)
        print(f"Agent responds: {response}")
        
        # Step 5: Speak the response
        speak_response(response)
        
        # Step 6: Perform specific actions (e.g., add to cart, checkout)
        if "cart_action" in matched_intents:
            if "add to cart" in text:
                product = "Laptop"  # Example, ideally fetched from the user's query
                response = track_product_action(user_id, "add_to_cart", product)
                print(f"Agent responds: {response}")
                speak_response(response)
        
        if "checkout" in matched_intents:
            response = track_product_action(user_id, "checkout")
            print(f"Agent responds: {response}")
            speak_response(response)
        
        # Step 7: End conversation if intent is goodbye
        if "goodbye" in matched_intents:
            print("Ending conversation...")
            break

# Start the conversation
conversation()
