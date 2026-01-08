import json
import yaml
import os
from openai import OpenAI

with open('src/config/model.yaml', 'r') as file:
    config_data = yaml.safe_load(file)

class RAGEvaluator:
    def __init__(self, llm_client):
        self.llm =  OpenAI(
                        base_url="https://api.groq.com/openai/v1",
                        api_key= os.environ['API_KEY']
                    )

   

    def evaluate_response(self, query, context, answer ,history):

        eval_prompt = f"""
        Evaluate the following RAG response.
        Query: {query}
        Context: {context}
        Answer: {answer}
        History: {history}

        Evaluation Rules:
        1. If the Query is a general greeting or unrelated to the context, relevance should be 1.0 and hallucination should be false if the LLM responds politely.
        2. faithfulness_score (0-1): If context is provided, does the answer stay true to it? If no context is relevant, mark as 1.0 as long as the LLM doesn't make up fake facts about the context.
        3. relevance_score (0-1): Does it address the user's intent?
        4. hallucination_detected (bool): Only set to true if the LLM claims something is in the context when it is not. 

        Provide JSON only:
        """
        messages=[{"role": "system", "content": eval_prompt}]

        response = self.llm.chat.completions.create(
                        model=config_data["model_name"],
                        messages=messages,
                        response_format={"type": "json_object"}
                    ) 
        print(response.choices[0].message.content)
        return json.loads(response.choices[0].message.content)
    
