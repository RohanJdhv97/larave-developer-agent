import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("ANTHROPIC_API_KEY")
model = os.getenv("CLAUDE_MODEL")

# Claude API endpoint
api_url = "https://api.anthropic.com/v1/messages"

# Print the API key partially to verify it's loaded (but don't expose the full key)
print(f"API Key begins with: {api_key[:10]}...")
print(f"Using model: {model}")

# Headers
headers = {
    "x-api-key": api_key,
    "Content-Type": "application/json",
    "anthropic-version": "2023-06-01"
}

# Request data
data = {
    "model": model,
    "messages": [
        {"role": "user", "content": "What is the latest version of Laravel?"}
    ],
    "max_tokens": 1000
}

# Make the request
print("Sending request to Claude API...")
try:
    response = requests.post(api_url, headers=headers, json=data)
    print(f"Response status code: {response.status_code}")
    
    # Print response
    if response.status_code == 200:
        response_json = response.json()
        print("\nClaude's response:")
        print(response_json.get("content")[0].get("text"))
    else:
        print("Error response:")
        try:
            error_details = response.json()
            print(json.dumps(error_details, indent=2))
        except:
            print(response.text)
except Exception as e:
    print(f"Exception occurred: {str(e)}") 