import re
import json
from typing import List, Dict, Optional
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

def parse_unstructured_data(text: str) -> Dict[str, Optional[str]]:
    """Parses unstructured transaction data and extracts relevant fields."""
    
    extracted_data = {}
    
    # Define regex patterns for extracting information
    patterns = {
        "Transaction ID": r"(?:Transaction ID|TID):\s*(\S+)",
        "Date": r"Date:\s*([\d\- :]+)",
        "Amount": r"Amount:\s*\$([\d,]+\.\d{2})",
        "Currency Exchange": r"Currency Exchange:\s*(.*)",
        "Transaction Type": r"Transaction Type:\s*(.*)",
        "Reference": r"Reference:\s*\"(.*)\"",
        "Transaction Notes": r"Additional Notes:\s*(.*)"
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
        if match:
            extracted_data[key] = match.group(1).strip()
    
    # Extract Sender and Receiver information
    sender_match = re.search(r"Sender:\s*(.*?)Receiver:", text, re.DOTALL)
    receiver_match = re.search(r"Receiver:\s*(.*?)(Amount:|Additional Notes:|$)", text, re.DOTALL)
     
    sender_info = {}
    receiver_info = {}
    
    if sender_match:
        sender_text = sender_match.group(1).strip()
        
        # Extract Sender Name
        sender_name_match = re.search(r"• Name:\s*\"([^\"]+)\"", sender_text)
        sender_info["Name"] = sender_name_match.group(1).strip() if sender_name_match else None
        
        # Extract Sender Account
        sender_account_match = re.search(r"• Account:\s*([^\n]+)", sender_text)
        sender_info["Account"] = sender_account_match.group(1).strip() if sender_account_match else None
        
        # Extract Sender Jurisdiction from Account
        if sender_info.get("Account"):
            jurisdiction_match = re.search(r"\(([^)]+)\)", sender_info["Account"])
            sender_info["Jurisdiction"] = jurisdiction_match.group(1).strip() if jurisdiction_match else None
        
        # Extract other Sender details dynamically
        other_sender_matches = re.findall(r"[\*•]\s*([a-zA-Z\s]+):\s*\"?([^\n\"]+)\"?", sender_text)
        for field_name, field_value in other_sender_matches:
            field_key = field_name.lower().replace(' ', '_')
            if field_key not in ["name", "account", "jurisdiction"]:  # Exclude core fields
                sender_info[field_key] = field_value.strip()
    
    if receiver_match:
        receiver_text = receiver_match.group(1).strip()
        
        # Extract Receiver Name
        receiver_name_match = re.search(r"• Name:\s*\"([^\"]+)\"", receiver_text)
        receiver_info["Name"] = receiver_name_match.group(1).strip() if receiver_name_match else None
        
        # Extract Receiver Account
        receiver_account_match = re.search(r"• Account:\s*([^\n]+)", receiver_text)
        receiver_info["Account"] = receiver_account_match.group(1).strip() if receiver_account_match else None
        
        # Extract Receiver Jurisdiction from Account
        if receiver_info.get("Account"):
            jurisdiction_match = re.search(r"\(([^)]+)\)", receiver_info["Account"])
            receiver_info["Jurisdiction"] = jurisdiction_match.group(1).strip() if jurisdiction_match else None
        
        # Extract other Receiver details dynamically
        other_receiver_matches = re.findall(r"[\*•]\s*([a-zA-Z\s]+):\s*([^\n]+)", receiver_text)
        for field_name, field_value in other_receiver_matches:
            field_key = field_name.lower().replace(' ', '_')
            if field_key not in ["name", "account", "jurisdiction"]:  # Exclude core fields
                receiver_info[field_key] = field_value.strip()
            
    extracted_data["Sender"] = sender_info
    extracted_data["Receiver"] = receiver_info
    
    return extracted_data

def identify_entity_type(name: Optional[str]) -> str:
    """Identifies entity type using spaCy NER."""
    if not name or not isinstance(name, str):
        return "Unknown"

    doc = nlp(name)
    
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            return 'Organization'
        elif ent.label_ in ['GPE', 'LOC']:
            return 'Jurisdiction'
        elif ent.label_ == 'PERSON':
            return 'Person'
    
    return 'Unknown'

def filter_entities(entities: List[Dict]) -> List[Dict]:
    """Filters entities to include only relevant types: organizations, persons, jurisdictions."""
    filtered_entities = []
    
    for entity in entities:
        if entity["Entity Name"].lower() not in ["eur - usd", "ofac sdn list", "011 equipment procurement'"]:
            filtered_entities.append(entity)
    
    return filtered_entities

def process_unstructured_transactions(unstructured_data: List[str]) -> List[Dict]:
    """Processes a list of unstructured transaction strings into structured format."""
    structured_transactions = []
    
    for data in unstructured_data:
        parsed_data = parse_unstructured_data(data)
        
        # Construct the structured transaction record
        transaction_record = {
            "Raw Transaction": data.strip(),
            "Transaction ID": parsed_data.get("Transaction ID", parsed_data.get("TID", "")),
            "Date": parsed_data.get("Date", ""),
            "Amount": parsed_data.get("Amount", ""),
            "Currency Exchange": parsed_data.get("Currency Exchange", ""),
            "Transaction Type": parsed_data.get("Transaction Type", ""),
            "Reference": parsed_data.get("Reference", ""),
            
            # Sender Details
            "Sender": {
                "Name": parsed_data["Sender"].get("Name"),
                "Account": parsed_data["Sender"].get("Account"),
                "Jurisdiction": parsed_data["Sender"].get("Jurisdiction"),
                "Additional Info": [
                    f"{k.capitalize().replace('_', ' ')}: {v}" 
                    for k, v in parsed_data["Sender"].items() 
                    if k not in ["Name", "Account", "Jurisdiction"]
                ]
            },
            
            # Receiver Details
            "Receiver": {
                "Name": parsed_data["Receiver"].get("Name"),
                "Account": parsed_data["Receiver"].get("Account"),
                "Jurisdiction": parsed_data["Receiver"].get("Jurisdiction"),
                "Additional Info": [
                    f"{k.capitalize().replace('_', ' ')}: {v}" 
                    for k, v in parsed_data["Receiver"].items() 
                    if k not in ["Name", "Account", "Jurisdiction"]
                ]
            },
            
            # Transaction Details
            "Transaction Details": {
                "Notes": parsed_data.get("Transaction Notes", "").splitlines() if parsed_data.get("Transaction Notes") else []
            },
            
            # Proper Noun Entities (Extracted using spaCy NER)
            "Proper Noun Entities": []
        }
        
        # Use spaCy to extract entities from the full text of the transaction
        doc = nlp(data)
        
        seen_entities = set()
        
        for ent in doc.ents:
            entity_info = {
                'Entity Name': ent.text,
                'Entity Type': identify_entity_type(ent.text)
            }
            
            if entity_info['Entity Type'] != 'Unknown' and ent.text not in seen_entities:
                transaction_record["Proper Noun Entities"].append(entity_info)
                seen_entities.add(ent.text)

        transaction_record["Proper Noun Entities"] = filter_entities(transaction_record["Proper Noun Entities"])

        structured_transactions.append(transaction_record)
    
    return structured_transactions

def read_unstructured_file(file_path: str) -> List[str]:
    """Reads unstructured data from a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip().split("\n---\n")  # Split by '---' delimiter 