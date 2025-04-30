import json
from transformers import pipeline

def analyze_entities(input_data):
    """
    Analyzes entities in the input data to determine criminal involvement and provides reasoning.
    
    Args:
        input_data (dict): Input JSON with entity descriptions.
    Returns:
        dict: Output JSON with analysis results.
    """
    # Load the Hugging Face text-generation pipeline with a free model
    try:
        generator = pipeline(
            "text-generation", 
            model="meta-llama/Llama-3.2-1B", 
            device=0  # Use device=0 for GPU or -1 for CPU
        )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize the model: {str(e)}")

    results = {}
    
    # Define the prompt template
    prompt_template = """
    You are a compliance officer tasked with determining whether an entity is involved in criminal activities based on a description. Use a chain-of-thought reasoning process to evaluate the information.
    
    For each entity:
    1. Evaluate if the entity is involved in any crime.
    2. If yes, categorize the crime(s) into the following categories:
       - Money Laundering
       - Tax Evasion
       - Terrorist Financing
       - Criminal Organization
       - Fraud
       - Data Privacy Violation
       - Environmental Violation
    3. Provide detailed reasoning for your conclusion.
    
    Here is the entity description:
    "{description}"
    
    Respond in JSON format:
    {{
        "Entity": "{entity_name}",
        "Crime(s)": [List of Crimes or "None"],
        "Reasoning": "{Your detailed reasoning}"
    }}
    """

    # Iterate over the input data
    for entity, description in input_data.items():
        try:
            # Correctly format the prompt
            prompt = prompt_template.format(
                entity_name=entity,
                description=description
            )
            
            # Generate the response using the model
            response = generator(
                prompt,
                max_length=512,
                do_sample=True,
                temperature=0.7,
                num_return_sequences=1
            )
            
            # Extract the generated text
            result_text = response[0]["generated_text"]
            
            # Try to parse the response into JSON
            try:
                result_json = json.loads(result_text)
            except json.JSONDecodeError:
                result_json = {
                    "Entity": entity,
                    "Crime(s)": ["Error"],
                    "Reasoning": f"Invalid JSON output from the model: {result_text[:200]}..."
                }
                
        except Exception as e:
            # Handle errors during generation
            result_json = {
                "Entity": entity,
                "Crime(s)": ["Error"],
                "Reasoning": f"An error occurred: {str(e)}"
            }
            
        results[entity] = result_json
    
    return results

def main():
    """Main function to run the entity analysis"""
    input_file = "entity_crimes.json"
    output_file = "output.json"
    
    try:
        # Load input JSON file
        with open(input_file, "r") as file:
            input_data = json.load(file)
            
        # Analyze the entities
        output_data = analyze_entities(input_data)
        
        # Save the results to an output JSON file
        with open(output_file, "w") as file:
            json.dump(output_data, file, indent=4)
            
        print(f"Analysis complete. Results saved to {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{input_file}'")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()