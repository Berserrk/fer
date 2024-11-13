import requests
import json
from leetcode import 

url = "http://localhost:11434/api/chat"

def llama3(prompt):
    data = {
        "model": "mistral",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if 'error' in response_json:
        raise Exception(f'API Error: {response_json['error']}')
    print("Full response:", response.text)  # Add this line
    return response.json()["message"]["content"]

response = llama3("who wrote the book godfather")

with open ("output.json", 'w') as f:
    json.dump(response, f, indent=4)
print(response)