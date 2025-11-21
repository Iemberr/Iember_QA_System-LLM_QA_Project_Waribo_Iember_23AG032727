"""
LLM Q&A Web Application
A simple web GUI for interacting with Hugging Face LLM API
"""

import os
import re
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)


def preprocess_question(question: str) -> str:
    """
    Apply basic preprocessing:
    - Lowercase
    - Remove extra whitespace
    - Remove special punctuation (keeping '?' for questions)
    """
    text = question.lower()
    text = ' '.join(text.split())
    text = re.sub(r'[^a-z0-9\s?.,!]', '', text)
    return text.strip()


def query_llm_api(question: str) -> dict:
    """
    Send the question to Hugging Face Router API.
    Uses the OpenAI-compatible chat completions endpoint.
    """
    api_token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not api_token:
        return {
            "error": "HUGGINGFACE_API_TOKEN environment variable not set."
        }
    
    # New Hugging Face Router endpoint (OpenAI-compatible)
    api_url = "https://router.huggingface.co/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_token.strip()}",
        "Content-Type": "application/json"
    }
    
    # Using Qwen 2.5 model (fast and free)
    payload = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "max_tokens": 250,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # Extract answer from OpenAI-compatible response
        if "choices" in result and len(result["choices"]) > 0:
            answer = result["choices"][0]["message"]["content"]
            return {"answer": answer.strip()}
        else:
            return {"error": f"Unexpected response format: {result}"}
    
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}


@app.route('/')
def home():
    """Render the main page"""
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle question submission"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid request: No JSON data received.'
            }), 400
        
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'error': 'Please enter a valid question.'
            }), 400
        
        # Preprocess question
        processed_question = preprocess_question(question)
        
        # Query LLM API
        result = query_llm_api(question)
        
        response_data = {
            'original_question': question,
            'processed_question': processed_question,
            'answer': result.get('answer', ''),
            'error': result.get('error', None)
        }
        
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}'
        }), 500


if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)
