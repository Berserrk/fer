import requests
import json
import time

url = "http://localhost:11434/api/generate"
categories_list = ["criminal", "fraud", "politics"]
rule = """
Task: You are an agent that is analyzing a JSON file.
Inputs:
1. JSON file: {json_file}
2. Provided list: {categories_list}
3. Entity to analyze: {entity}
Rules:
a. Analyze the {entity}, and if its value matches one of the categories present in the provided list {categories_list}
b. the categories field can have one or multiple label
c. If no label is found then give the label : "no label"
The output should be a JSON object containing the category "criminal" for the given entity.
Example:
{{
 "{entity}": {{"categories": [fraud, criminal]}}
}}
"""

def llama3(json_file, rule, categories_list, entity):
    prompt = rule.format(json_file=json.dumps(json_file), categories_list=categories_list, entity=entity)
    data = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    if 'error' in response_json:
        raise Exception(f'API Error: {response_json["error"]}')
    return response_json.get("response", "")

print("Starting the processing of entities...")

# Main execution
with open("entity_summary.json", 'r') as file:
    file_json = json.load(file)
print(f"Loaded {len(file_json)} entities from entity_summary.json")

def main():
    results = {}
    failed_entities = []

    for i, entity in enumerate(file_json, 1):
        print(f"\nProcessing entity {i} of {len(file_json)}: {entity}")
        start_time = time.time()
        try:
            response = llama3(
                json_file=file_json,
                rule=rule,
                categories_list=categories_list,
                entity=entity
            )
            results[entity] = json.loads(response)
            print(f"Categories for {entity}: {results[entity][entity]['categories']}")
        except Exception as e:
            print(f"Failed to process {entity}, reason: {e}")
            failed_entities.append(entity)
        end_time = time.time()
        print(f"Time taken: {end_time - start_time:.2f} seconds")

    # Retry failed entities
    if failed_entities:
        print(f"\nRetrying {len(failed_entities)} failed entities...")
        for entity in failed_entities:
            print(f"\nRetrying entity: {entity}")
            start_time = time.time()
            try:
                response = llama3(
                    json_file=file_json,
                    rule=rule,
                    categories_list=categories_list,
                    entity=entity
                )
                results[entity] = json.loads(response)
                print(f"Categories for {entity}: {results[entity][entity]['categories']}")
            except Exception as e:
                print(f"Failed to process {entity} on retry, reason: {e}")
            end_time = time.time()
            print(f"Time taken: {end_time - start_time:.2f} seconds")

    print("\nAll entities processed. Saving results...")
    with open("output.json", 'w') as f:
        json.dump(results, f, indent=2)
    print("Results saved to output.json")


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"total Time taken: {end_time - start_time:.2f} seconds")
