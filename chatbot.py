from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini API (make sure GOOGLE_API_KEY is set in your environment)
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def get_gemini_response(prompt):
    """Gets a response from the Gemini API."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "I'm sorry, I encountered an error. Please try again later."

    # **Streaming Example (Requires Frontend Changes):**
    #   For longer responses, streaming significantly improves perceived speed.
    #   This involves:
    #     1.  Using `model.generate_content(prompt, stream=True)`
    #     2.  Iterating through the `response.parts` (each part is a chunk of text)
    #     3.  Sending each chunk to the frontend via Server-Sent Events or WebSockets
    #   The frontend needs to be adapted to handle the streamed data.
    # try:
    #     response = model.generate_content(prompt, stream=True)
    #     for chunk in response:
    #         yield chunk.text  # Yield chunks to the frontend (SSE or WebSockets)
    # except Exception as e:
    #     print(f"Error calling Gemini API: {e}")
    #     yield "I'm sorry, I encountered an error. Please try again later." # Yield an error message
@app.route("/")  # Landing page route
def index():
    return render_template("index.html")
@app.route("/chatbot")  # Chatbot page route
def chatbot_page():
    return render_template("chatbot.html")  # Render the HTML page

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["user_message"]
    prompt = f"You are a supportive mental health chatbot named Zenova. A user says: '{user_message}'. Respond in a helpful and empathetic way. If the message is not related to mental health, respond with 'Sorry, I can only assist with mental health-related queries.'"
    gemini_response = get_gemini_response(prompt)
    return jsonify({"response": gemini_response}) # Send the response back as JSON

#if __name__ == "__main__":
#    app.run(debug=True)  # Enable debug mode for development