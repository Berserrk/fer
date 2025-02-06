import json
import re

def convert_json_to_string(file_path):
    # Read the JSON file
    with open(file_path, 'r') as file:
        json_content = json.load(file)
    
    # Convert to string with indentation
    json_str = json.dumps(json_content, indent=2)
    
    # Remove quotes from keys using regex
    # This pattern matches quoted keys in JSON
    unquoted = re.sub(r'"(\w+)":', r'\1:', json_str)
    
    return unquoted

# Example usage
file_path = 'your_file.json'  # Replace with your JSON file path
result = convert_json_to_string(file_path)
print(result)

# Optionally save to a new file
with open('converted_output.txt', 'w') as f:
    f.write(result)
