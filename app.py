from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import requests
import pandas as pd
import time

app = Flask(__name__)
# API DETAILS
account_sid = "AC5dcaf95819e843bb94a6a8ea550957c2"
auth_token = "95c126fd0a4c1381de14208a4c46d8c5"
twilio_number = "+16813993451"

# DATA LOADING TO GET PHONE NUMBERS ON BASIS OF STATUS
data = pd.read_csv("deploy/CRM_Data.csv")
stat_priority = {"Hot": 1, "Warm": 2, "Cold": 3}

data["Priority"] = data["Status"].map(stat_priority)
final_data = data.sort_values(by="Priority")

# MAKING THE CALL
def call(to_number, name, status):
    print(f"Initiating call to {name} ({to_number}) - Status: {status}")
    try:
        # Make the call
        call = client.calls.create(
            to=to_number,
            from_=twilio_number,
            url="https://your-app-name.vercel.app/voice"  # TwiML endpoint
        )
        print(f"Call to {name} successfully initiated. Call SID: {call.sid}")
    except Exception as e:
        print(f"Failed to initiate call to {name}. Error: {str(e)}")

# Endpoint for Twilio to serve TwiML during the call
@app.route("/voice", methods=["POST"])
def handle_voice():
    response = VoiceResponse()
    response.say("Hello! Thank you for contacting us.")
    response.pause(length=1)
    response.say("How can I assist you today? Please respond after the beep.")
    response.record(max_length=30, play_beep=True, action="/process_response", timeout=5)
    return str(response)

# Endpoint to process the recorded response
@app.route("/process_response", methods=["POST"])
def process_response():
    recording_url = request.form.get("RecordingUrl")
    print(f"Recording URL: {recording_url}")

    # Download the audio file from the recording URL
    audio_file = download_audio(recording_url)

    # Step 1: Convert audio to text using Speech Recognition
    text = convert_audio_to_text(audio_file)

    # Step 2: Process the text (NLU)
    intent = match_intent(text)
    print(f"Matched intent: {intent}")

    # Step 3: Generate a dynamic response
    response_text = respond(intent)
    print(f"Response to customer: {response_text}")

    # Step 4: Create a Twilio VoiceResponse with the generated text
    response = VoiceResponse()
    response.say(response_text)
    response.pause(length=1)
    response.say("Is there anything else you would like to ask?")
    response.record(max_length=30, play_beep=True, action="/process_response", timeout=5)
    return str(response)

# Function to download audio file
def download_audio(recording_url):
    import requests
    response = requests.get(recording_url)
    audio_file = "recording.wav"
    with open(audio_file, "wb") as f:
        f.write(response.content)
    return audio_file

# Function to convert audio to text
def convert_audio_to_text(audio_file):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
            print(f"Recognized text: {text}")
            return text
    except sr.UnknownValueError:
        return "I couldn't understand the audio."
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"

# Function to match intent
def match_intent(text):
    intents = {
        "greeting": ["hello", "hi", "hey", "good morning", "good evening", "hey there"],
        "product_inquiry": ["tell me about your product", "what do you sell", "give me more info about your products"],
        "price_inquiry": ["how much does it cost", "what is the price", "pricing details", "how much is it"],
        "thank_you": ["thank you", "thanks", "appreciate it"],
        "goodbye": ["bye", "goodbye", "see you", "later", "talk to you soon"],
    }
    text = text.lower()
    for intent, keywords in intents.items():
        if any(keyword in text for keyword in keywords):
            return intent
    return "default"

# Function to generate response
def respond(intent):
    responses = {
        "greeting": "Hello! How can I assist you with your purchase today?",
        "product_inquiry": "We offer a variety of products, including electronics, home appliances, and accessories. Which category interests you?",
        "price_inquiry": "Our products range from $10 to $500 depending on the item. What product are you interested in?",
        "thank_you": "You're welcome! I'm here to help.",
        "goodbye": "Goodbye! Have a great day, and thank you for your interest in our products!",
        "default": "I'm sorry, I didn't quite catch that. Could you please repeat?"
    }
    return responses.get(intent, "I'm sorry, I didn't quite catch that. Could you please repeat?")

# Loop through the sorted CRM data and call customers
for index, row in final_data.iterrows():
    name = row["Customer Name"]
    phone = row["Phone No."]
    status = row["Status"]

    # Initiate a call to each customer
    call(phone, name, status)
    time.sleep(2)  # Delay to avoid overwhelming API calls

print("All calls completed.")

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)