1. Entity recognition: 
    - Spacy to find entities: can't find "the president" 
    because Spacy has been trained on name. Need coreference resolution that will link pronouns and nouns back to the correct entities.
    - use coref-spanbert?
2. to find clustering now?
    - sentence transformer with a model all-MiniLM-L6-v2
    - fuzzy name matching 
3. To summarize 



# GLINER
GLiNER (Generalist Model for Named Entity Recognition) is an advanced model designed for Named Entity Recognition (NER) tasks, which are crucial in Natural Language Processing (NLP) applications. This model is built to identify any type of entity using a bidirectional transformer encoder, similar to BERT, making it a versatile tool for NER tasks.
Key Features of GLiNER
	•	Generalist Approach: Unlike traditional NER models that are limited to predefined entity types, GLiNER can recognize a wide range of entities through natural language instructions. This flexibility allows it to adapt to various contexts and applications.ntial token generation of large language models (LLMs). It has demonstrated strong performance, outperforming models like ChatGPT and fine-tuned LLMs in zero-shot evaluations across different NER benchmarks.
	•	Resource-Friendly: The model is designed to be compact and efficient, making it suitable for scenarios with limited computational resources. This contrasts with the high cost and size of LLMs, particularly those accessed via APIs like ChatGPT.
Technical Details
	•	Architecture: GLiNER uses a BERT-like bidirectional transformer encoder. It encodes both entity types and text spans into a unified latent space, allowing effective comparison between them. This involves generating embeddings for each possible span in the text and matching these with entity type embeddings using a dot product and sigmoid activation function.
	•	Training and Evaluation: The model is trained on datasets like Pile-NER, utilizing techniques such as Binary Cross-Entropy Loss to maximize correct span-entity pairings while minimizing incorrect ones. This training approach enhances its ability to accurately classify entities across diverse datasets.
GLiNER represents a significant advancement in the field of NER by combining flexibility, efficiency, and strong performance in a resource-friendly package.

- Bidirectional Transformer Encoder: Key Notes
	•	Definition: A neural network architecture for NLP that processes text in both forward and backward directions.
	•	Bidirectional Processing: Captures context from both sides of each word, enhancing understanding of meaning.
	•	Transformer Architecture: Utilizes self-attention mechanisms to weigh the importance of words and capture long-range dependencies.
	•	Applications: Used in models like BERT, excelling in tasks such as named entity recognition, sentiment analysis, and question answering.
	•	Advantage: Provides nuanced and comprehensive language representations.



	jj reddick 
	