Sure! Here’s a more polished and expanded version of your text, with improved clarity, structure, and flow while keeping the original ideas intact:

⸻

Article Detective – Overview

Article Detective is a powerful application designed to assist users in analyzing articles—particularly investigative or journalistic pieces—with the aim of identifying individuals or organizations potentially involved in criminal activities. The app currently supports document uploads in .docx format, with PDF support under testing and scheduled for release by the end of April.

At its core, Article Detective leverages advanced natural language processing and large language models (LLMs) to parse, analyze, and cross-reference article content with a historical entity database. This enables users to not only understand the content of the articles they upload but also uncover connections, patterns, and red flags tied to potential criminal behavior.

⸻

Key Features

1. Multi-Document Upload & Intelligent Processing

Users can upload one or multiple articles at once. Upon upload, the application triggers a pipeline of Python scripts powered by LLMs, which perform a series of analytical steps:
	•	Summary Generation: Condensed overviews of each article.
	•	Entity Extraction: Identification of people, organizations, and other relevant entities mentioned.
	•	Entity Resolution: Grouping and consolidating variations of the same entity.
	•	Entity Exclusion: Filtering out irrelevant or already-known entities.
	•	Entity Categorization: Sorting entities into first-degree (direct involvement) and second-degree (indirect connection) categories.
	•	Relationship Mapping: Identifying and outlining links between entities.

If an article has already been processed before, the app retrieves the previously generated data from the database instead of re-processing, ensuring faster response times and optimized resource usage.

Upcoming Enhancements:
	•	Ability to define and customize the list of crimes the system should flag.
	•	Option to predefine a list of entities to be excluded before analysis—ideal for users who already possess context-specific knowledge.

⸻

2. Article Summarization

This feature offers an intelligent, layered summary of uploaded content:
	•	For a single article, users receive a concise summary paragraph.
	•	For multiple articles, individual summaries are generated for each article, followed by a composite overview. This final summary emphasizes common threads, shared entities, and potential interconnections between different pieces.

⸻

3. Activities Table (Entity Flagging Dashboard)

This interactive HTML table displays all entities identified and assessed by the system, particularly in relation to the list of crimes provided by the user or pre-set in the application.

Each row represents an entity, and columns include:
	•	Crime indicators (green checkmarks for confirmed involvement, red crosses otherwise),
	•	A textual description of the entity,
	•	A flag status (based on the presence of any criminal activity),
	•	Editable comment fields.

User Interaction Capabilities:
	•	Customize Table View: Remove or re-add columns dynamically using the interface.
	•	Edit Data: Change flag status, add or remove crimes, provide comments, and update entity summaries directly in the table.
	•	Database Sync: All modifications are saved to the central database, improving data quality and reinforcing future analysis.

Upcoming Feature:
	•	Integration of historical data insights to further refine flagged entities, drawing on past trends and patterns for enhanced accuracy.

⸻

4. Entity Relationships Graph

This visually rich graph represents entity connections using a node-edge style interface:
	•	Displays both directly flagged entities and those indirectly linked.
	•	Shows the type of relationship using seven predefined categories: owner, investor, partner, shareholder, representative, beneficiary, and other.

Interactive Capabilities:
	•	Full-screen mode for detailed analysis.
	•	Zoom and drag to explore complex networks.
	•	Click on an entity to highlight first-degree connections in red and open a detailed information box on the side.

Planned Upgrade:
	•	The graph will incorporate historical interactions and known relationships from the database to enrich visual insights.
	•	Potential transition to customizable relationship types defined by business users for increased domain relevance.

⸻

5. Entity Summary Browser

This feature offers a scrollable list of all entities extracted from the articles. When selecting an entity, users see:
	•	A detailed description of the entity,
	•	A breakdown of its crime categorization (as flagged by the system).

Future Update:
	•	If the entity already exists in the database, its description will be refreshed and enhanced using existing data—providing a more complete and updated view over time.

⸻

6. Manual Entity Addition

To complement automated analysis, users have the ability to manually input entities into the system. This includes:
	•	The entity’s name,
	•	Associated crimes,
	•	A custom summary.

Once added, this data is stored in the main database and becomes part of future document analyses. If a manually-added entity appears in later uploads, the system will more accurately identify and flag it based on the existing record.

⸻

A Living System: The More You Use It, the Better It Gets

Article Detective is built on the principle of continuous improvement. Every article processed, every entity flagged, and every manual input contributes to a growing, smarter database. As the system ingests more data, its ability to detect criminal activity and map complex networks becomes increasingly sophisticated.

In short: the more it’s used, the more powerful it becomes.

⸻

Let me know if you’d like this turned into a webpage layout, PDF brochure, or product doc—happy to help shape it however you need.
