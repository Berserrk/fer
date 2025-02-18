You are given a list of entity names. Your task is to identify and keep only the proper names of specific people and organizations, while strictly removing generic roles, job titles, pronouns, and vague references.

Instructions:
	1.	Analyze each entity and determine if it is a proper name of a person or an organization.
	2.	Justify your decision by explaining why the entity is either included or excluded.
	3.	Return a structured JSON output with both the filtered entities and the reasoning for exclusion.

Inclusion Rules:

✅ Keep Only:
	•	Names of specific people (e.g., "Barack Obama", "Marie Curie").
	•	Names of organizations, companies, or institutions (e.g., "Google", "United Nations", "NASA").

Strict Exclusion Rules:

❌ Remove and Explain Why:
	•	General job titles (e.g., "officials", "senior officials", "managers", "chairman", "director") → These are roles, not specific entities.
	•	Pronouns and vague references (e.g., "he", "she", "they", "spokesperson") → These do not refer to named entities.
	•	Non-specific group names (e.g., "the administration", "the board", "government representatives") → These do not indicate a proper name.
