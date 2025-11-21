"""
LLM Q&A CLI Application
This script accepts a natural-language question, preprocesses it,
sends it to Hugging Face Inference API, and displays the answer.
"""

import os
import re
import requests
from typing import Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def preprocess_question(question: str) -> str:
    """
    Apply basic preprocessing:
    - Lowercase
    - Remove extra whitespace
    - Remove special punctuation (keeping '?' for questions)
    """
    # Lowercase
    text = question.lower()
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove special characters except alphanumeric, spaces, and basic punctuation
    text = re.sub(r'[^a-z0-9\s?.,!]', '', text)
    return text.strip()


def query_llm_api(question: str) -> Dict:
    """
    Send the question to Hugging Face Router API.
    Uses the OpenAI-compatible chat completions endpoint.
    Requires HUGGINGFACE_API_TOKEN environment variable.
    """
    api_token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not api_token:
        return {
            "error": "HUGGINGFACE_API_TOKEN environment variable not set. "
                     "Please set it with your Hugging Face API token."
        }
    
    # New Hugging Face Router endpoint (OpenAI-compatible)
    api_url = "https://router.huggingface.co/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_token.strip()}",
        "Content-Type": "application/json"
    }
    
    # Using Qwen 2.5 Coder model (fast and free)
    payload = {
        "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
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


def main():
    """Main CLI loop"""
    print("=" * 60)
    print("Welcome to the LLM Question & Answering CLI")
    print("Powered by Hugging Face Qwen 2.5 Coder")
    print("=" * 60)
    print("\nType 'exit' or 'quit' to end the session.\n")
    
    while True:
        # Get user question
        user_input = input("Your Question: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("\nThank you for using the LLM Q&A CLI. Goodbye!")
            break
        
        if not user_input:
            print("Please enter a valid question.\n")
            continue
        
        # Preprocess question
        processed = preprocess_question(user_input)
        print(f"\nProcessed Question: {processed}")
        
        # Query LLM API
        print("Querying LLM API...\n")
        result = query_llm_api(user_input)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}\n")
        else:
            print(f"💡 Answer:\n{result['answer']}\n")
        
        print("-" * 60 + "\n")


if __name__ == "__main__":
    main()
