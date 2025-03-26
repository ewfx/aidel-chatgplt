import json
from preRiskScore import Transaction
from riskScore import process

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
        output['supportingEvidence']=dict['resources']
        # output['supportingEvidence'] = 'Sample evidence data'
        # output['reason'] = 'Sample reason for risk assessment'
        # output['extractedEntities'] = ['Entity1', 'Entity2', 'Entity3'] 
        response.append(output)
    return response

