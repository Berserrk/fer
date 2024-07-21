'''
- Create ` a hugging face  user acces token 


-  “Initialize the LLM and the toolkit”
- initialize the agent
- define streamlit session state
- define the logic application whenever a user makes a query 
- run the application with the terminal by : streamlit run llm.py

- Mistral AI : 
- transformer decoder only 
- Mistral 7B v01 Group query attention (GQA) and sliding window attention (SWA):
    both improve the effiency and performance  of the LLM 

    

LMM
need :
- idea : if we combine single-modal models one for each data format we want to process and then use LLM as the brain of our agent to interact with those model 


3 ways :
- Azure Cognitive Services toolkit : “offers native integrations toward a set of AI models that can be consumed via API,”
- agentic custom approach : “select single models and tools (including defining custom tools) and concatenate them into a single agent that can leverage all of them”
- hardcoded approach: “we are going to build separate chains and combine them into a sequential chain.

'''
'''
coreruler_ner : run  the pipeline 
rules: utilise les output pour verifier les rules dessus
'''