import json
from typing import List, Dict, Optional
from gemini import get_country_llm

class Transaction:
    """Class to represent a transaction for risk scoring."""
    def __init__(
        self,
        country1: str,
        country2: str,
        intermediary: Optional[str] = None,
        e1: str = "",
        e2: str = "",
        e_intermediary: Optional[str] = None,
        persons: Optional[List[str]] = None,
        entities: Optional[List[str]] = None,
        jurisdictions: Optional[List[str]] = None,
        amount: float = 0,
        risky_entity: int = 0
    ):
        self.country1 = country1
        self.country2 = country2
        self.intermediary = intermediary or ""
        self.e1 = e1
        self.e2 = e2
        self.e_intermediary = e_intermediary or ""
        self.persons = persons or []
        self.entities = entities or []
        self.jurisdictions = jurisdictions or []
        self.amount = amount
        self.risky_entity = risky_entity

    @classmethod
    def from_processed_transaction(cls, transaction: Dict) -> 'Transaction':
        country_llm=get_country_llm(transaction)
        """Create a Transaction object from a processed transaction dictionary."""
        # Extract sender and receiver information
        sender = transaction.get('Sender', {})
        receiver = transaction.get('Receiver', {})
        
        # Extract amount (remove currency symbol and convert to float)
        amount_str = transaction.get('Amount', '0')
        if amount_str == '':
            amount = 0
        else:
            amount = float(amount_str.replace('$', '').replace(',', ''))
        
        # Extract persons and entities from Proper Noun Entities
        persons = []
        entities = []
        jurisdictions = []
        entities_section = transaction.get('Proper Noun Entities', [])
        for entity in entities_section:
            if entity.get('Entity Type') == 'Person':
                persons.append(entity['Entity Name'])
            elif entity.get('Entity Type') == 'Organization':
                entities.append(entity['Entity Name'])
            elif entity.get('Entity Type') == 'Jurisdiction':
                jurisdictions.append(entity['Entity Name'])
        for jurisdiction in jurisdictions:
            if jurisdiction!=sender.get('Jurisdiction', '') and jurisdiction!=receiver.get('Jurisdiction', ''):
                country_intermediary = jurisdiction
                break
        for entity in entities:
            if entity!=sender.get('Name', '') and entity!=receiver.get('Name', ''):
                e_intermediary = entity
                break
        # Create transaction object
        return cls(
            country1=country_llm['sender_country'] or sender.get('Jurisdiction', ''),
            country2=country_llm['reciever_country'] or receiver.get('Jurisdiction', ''),
            intermediary=country_intermediary,
            e1=sender.get('Name', ''),
            e2=receiver.get('Name', ''),
            e_intermediary=e_intermediary,
            persons=persons,
            entities=entities,
            jurisdictions=jurisdictions,
            amount=amount,
            risky_entity=1  # Will be determined later
        )
        
    
