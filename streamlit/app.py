Task: Analyze a single key from a JSON file, label it with predefined categories, and provide a suggestion.

Input:
1. Key name: [KEY_NAME]
2. Key value: [KEY_VALUE]
3. Predefined categories: [LIST_CATEGORIES_HERE]

Instructions:
1. Examine the provided key name and value.
2. Determine if the key matches one or more categories from the predefined list.
3. Create a brief suggestion explaining the categorization or potential use of the key.
4. Output a JSON object with the following structure:
   {
     "key": "[KEY_NAME]",
     "categories": [...],
     "suggestion": "..."
   }

Output Constraints:
1. "categories": List of matching category names. Use ["no label"] if no categories match.
2. "suggestion": Brief explanation or suggestion, under 15 words.
3. Adhere to the provided GBNF grammar for output structure.
4. Prioritize speed and accuracy.

Example Output:
{
  "key": "user_age",
  "categories": ["demographic", "personal_info"],
  "suggestion": "Age data for user segmentation and age-restricted content."
}

qwe