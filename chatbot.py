from flask import Flask, render_template, request, jsonify, send_from_directory
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables (for local development)

chatbot = Flask(__name__, static_folder='public', template_folder='public/templates')

# Configure Gemini API (make sure GOOGLE_API_KEY is set in Vercel or .env)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    print("WARNING: GOOGLE_API_KEY not found. Chatbot functionality will be disabled.")
    model = None  # Disable the model if no key is found

def get_gemini_response(prompt):
    """Gets a response from the Gemini API."""
    if model is None:
        return "Sorry, the chatbot is currently unavailable. Please check back later." #Return a default message if key not found
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "I'm sorry, I encountered an error. Please try again later."

# Serve static files (CSS, JavaScript, images) from the 'public' directory
@chatbot.route('/<path:path>')
def serve_static(path):
    return send_from_directory('public', path)

# Serve the index.html file (landing page)
@chatbot.route("/")
def index():
    return render_template("index.html")

# Chatbot page route - Serve chatbot.html from the 'public' directory
@chatbot.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")

@chatbot.route("/api/get_response", methods=["POST"]) #Updated Endpoint
def get_response():
    if model is None:
        return jsonify({"response": "Sorry, the chatbot is currently unavailable."}) #Return a default message if key not found
    user_message = request.form["user_message"]
    prompt = f"You are a supportive mental health chatbot named Zenova. A user says: '{user_message}'. Respond in a helpful and empathetic way. If you are unable to answer a question, respond with 'Sorry, I don't have an answer to that.'"
    gemini_response = get_gemini_response(prompt)
    return jsonify({"response": gemini_response}) # Send the response back as JSON

# This part is ONLY for LOCAL development. Vercel ignores it.
if __name__ == "__main__":
    chatbot.run(debug=True, port=5000)  # Enable debug mode for development