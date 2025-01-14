from flask import Flask, render_template, request, jsonify
import openai

# Initialize the Flask app
app = Flask(__name__)

# OpenAI API configuration
openai.api_key = "your_openai_api_key_here"  # Replace with your OpenAI API key

def get_response_from_openai(user_input):
    """Fetch response from OpenAI's API."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the desired OpenAI model
            prompt=f"User: {user_input}\nAI:",
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=["User:", "AI:"]
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error fetching response from OpenAI: {e}")
        return "Sorry, there was an error processing your request."

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle conversation
@app.route('/conversation', methods=['POST'])
def conversation():
    user_input = request.json.get("text", "")
    response = get_response_from_openai(user_input)
    return jsonify({"response": response})

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
