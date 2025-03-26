import json
from preRiskScore import Transaction
from riskScore import process
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
import json

def invoke_groq_cloud(research_object: str)-> str:
       
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    client = Groq(
        api_key=GROQ_API_KEY,
    )

    system_prompt = """
                    You are an excellent financial analyst. You must strictly base your response on the provided research content and not invent any details beyond it. Analyze the content to determine the riskiness of the transaction in the 'Raw Transaction' property. Your output must be a single JSON object with the following keys:
                - "reason": Provide a concise explanation of the risk assessment using direct evidence from the research.
                - "supportingEvidence": List one or more URLs from the research content that support your justification.
                - "extractedEntities": The name of the entity involved. This will be array
                - "entityTypes": The type of entity (e.g., corporation, individual). This will be array corresponding enity_names
                - "risk_factor": A classification of the risk (either "high", "medium", or "low").
                - "confidence": Indicate your confidence level in this analysis (e.g., on a scale or descriptive term).

                Do not include any text besides the JSON object. The research content will be provided as a parameter in the user prompt.

                """
    user_prompt = """

                Analyze the following transaction object and provide your risk analysis for the transaction with proper justification and evidence (URLs) for risk score given. Output only a JSON object with the keys specified.

                Research Content: {research_content}
    
                """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt.format(research_content=str(research_object))},
            
        ],
        temperature=0.1,
        max_completion_tokens=3640,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def load_transactions(file_path: str) -> list:
    """
    Load transactions from a JSON file and return them as a list of dictionaries.
    
    Args:
        file_path: Path to the JSON file containing transactions
        
    Returns:
        List of dictionaries containing transaction data
    """
    try:
        with open(file_path, 'r') as f:
            transactions = json.load(f)
        return transactions
    except Exception as e:
        print(f"Error loading transactions: {str(e)}")
        return []

def risk_entry():
    """
    Main function to demonstrate loading transactions.
    """
    # Path to the JSON file
    file_path = "data/processed_transactions.json"
    
    # Load transactions
    transactions = load_transactions(file_path)
    print(risk_response(transactions))
    return risk_response(transactions)
    # Print some information about the loaded data

def risk_response(transactions):
    response=[]
    for transaction in transactions:
        output={}
        trans_obj = Transaction.from_processed_transaction(transaction)
        dict=process(trans_obj)
        # output['transactionId'] = transaction.get('Transaction ID', '')
        output['riskScore'] = dict['score']
        output['confidenceScore'] = dict['confidence_score']
        output['supporting_Evidence']=dict['resources']
        # output['reason'] = 'Sample reason for risk assessment'
        # output['extractedEntities'] = ['Entity1', 'Entity2', 'Entity3'] 
        combined_res = transaction | output
        justify_obj = invoke_groq_cloud(combined_res)
        justify_obj_dict = json.loads(justify_obj)
        final_obj = combined_res | justify_obj_dict
        response.append(final_obj)
    return response