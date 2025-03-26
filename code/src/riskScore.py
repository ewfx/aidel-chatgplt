import requests
import json
import time
from bs4 import BeautifulSoup
from risk_data import (
    fatf_black, fatf_grey, fatf_grey_2024, fatf_black_2024,
    corruption_data, basel_score
)
from preRiskScore import Transaction

class RiskDetails:
    """Class to store risk-related details for entities involved in a transaction."""
    def __init__(self):
        # FATF ratings (current)
        self.curr_fatf_e1 = 0
        self.curr_fatf_e2 = 0
        self.curr_fatf_intermediary = 0
        
        # FATF ratings (historical)
        self.hist_fatf_e1 = 0
        self.hist_fatf_e2 = 0
        self.hist_fatf_intermediary = 0
        
        # Sanctioned entity flags
        self.sanct_entity_e1 = 0
        self.sanct_entity_e2 = 0
        self.sanct_entity_intermediary = 0
        
        # Corruption scores
        self.corruption_score_e1 = 0
        self.corruption_score_e2 = 0
        self.corruption_score_intermediary = 0
        
        # Industry risk flag
        self.high_risk_industry = 0
        
        # Basel AML scores
        self.basel_score_e1 = 0
        self.basel_score_e2 = 0
        self.basel_score_intermediary = 0


def set_fatf(risk_details, country1, country2, intermediary):
    """Set FATF ratings for countries based on current FATF black and grey lists.
    
    Args:
        risk_details: RiskDetails object to update
        country1: First country name
        country2: Second country name
        intermediary: Intermediary country name
    """
    for element in fatf_black:
        if country1.lower() == element.lower():
            risk_details.curr_fatf_e1 = 1
        if country2.lower() == element.lower():
            risk_details.curr_fatf_e2 = 1
        if intermediary.lower() == element.lower():
            risk_details.curr_fatf_intermediary = 1
    
    for element in fatf_grey:
        if country1.lower() == element.lower():
            risk_details.curr_fatf_e1 = 1
        if country2.lower() == element.lower():
            risk_details.curr_fatf_e2 = 1
        if intermediary.lower() == element.lower():
            risk_details.curr_fatf_intermediary = 1


def set_fatf_hist(risk_details, country1, country2, intermediary):
    """Set historical FATF ratings for countries based on 2024 FATF black and grey lists.
    
    Args:
        risk_details: RiskDetails object to update
        country1: First country name
        country2: Second country name
        intermediary: Intermediary country name
    """
    for element in fatf_black_2024:
        if country1.lower() == element.lower():
            risk_details.hist_fatf_e1 = 1
        if country2.lower() == element.lower():
            risk_details.hist_fatf_e2 = 1
        if intermediary.lower() == element.lower():
            risk_details.hist_fatf_intermediary = 1
    
    for element in fatf_grey_2024:
        if country1.lower() == element.lower():
            risk_details.hist_fatf_e1 = 1
        if country2.lower() == element.lower():
            risk_details.hist_fatf_e2 = 1
        if intermediary.lower() == element.lower():
            risk_details.hist_fatf_intermediary = 1


def check_sanctioned_entity(entity_name):
    """Checks if an entity has search results on OpenSanctions.org.

    Args:
        entity_name (str): The name of the entity to search for.

    Returns:
        bool: True if search results are found, False otherwise.
    """
    if not entity_name:
        return False
    
    entity_name = entity_name.replace(" ", "+")
    url = f"https://www.opensanctions.org/search/?scope=securities&q={entity_name}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, "html.parser")

        # Check for the presence of search results
        results = soup.find_all("div", class_="Search_resultTitle__twair") 
        results2 = soup.find_all("span", class_="badge bg-warning")
        
        check_flag = False
        for result in results2:
            if result.text == "Sanctioned entity":
                check_flag = True
                break
        return len(results2) > 0 and check_flag

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return False


def set_sanctioned_entity_val(risk_details, e1, e2, intermediary):
    """Set sanctioned entity flags for entities.
    
    Args:
        risk_details: RiskDetails object to update
        e1: First entity name
        e2: Second entity name
        intermediary: Intermediary entity name
    """
    if check_sanctioned_entity(e1):
        risk_details.sanct_entity_e1 = 1
    if check_sanctioned_entity(e2):
        risk_details.sanct_entity_e2 = 1
    if check_sanctioned_entity(intermediary):
        risk_details.sanct_entity_intermediary = 1





def set_corruption_rank(risk_details, country1, country2, intermediary):
    """Set corruption scores for countries.
    
    Args:
        risk_details: RiskDetails object to update
        country1: First country name
        country2: Second country name
        intermediary: Intermediary country name
    """
    if country1 in corruption_data:
        risk_details.corruption_score_e1 = corruption_data[country1]
    if country2 in corruption_data:
        risk_details.corruption_score_e2 = corruption_data[country2]
    if intermediary in corruption_data:
        risk_details.corruption_score_intermediary = corruption_data[intermediary]


def set_basel_score(risk_details, country1, country2, intermediary):
    """Set Basel AML scores for countries.
    
    Args:
        risk_details: RiskDetails object to update
        country1: First country name
        country2: Second country name
        intermediary: Intermediary country name
    """
    if country1 in basel_score:
        risk_details.basel_score_e1 = basel_score[country1]
    if country2 in basel_score:
        risk_details.basel_score_e2 = basel_score[country2]
    if intermediary in basel_score:
        risk_details.basel_score_intermediary = basel_score[intermediary]


# Normalization functions
def fatf_norm(risk_details):
    """Normalize FATF ratings.
    
    Args:
        risk_details: RiskDetails object
        
    Returns:
        float: Normalized FATF score
    """
    present = (risk_details.curr_fatf_e1 + risk_details.curr_fatf_e2 + risk_details.curr_fatf_intermediary) / 3
    past = (risk_details.hist_fatf_e1 + risk_details.hist_fatf_e2 + risk_details.hist_fatf_intermediary) / 3
    return 0.7 * present + 0.3 * past


def corruption_norm(risk_details):
    """Normalize corruption scores.
    
    Args:
        risk_details: RiskDetails object
        
    Returns:
        float: Normalized corruption score
    """
    return (risk_details.corruption_score_e1 + risk_details.corruption_score_e2 + 
            risk_details.corruption_score_intermediary) / 300


def basel_norm(risk_details):
    """Normalize Basel AML scores.
    
    Args:
        risk_details: RiskDetails object
        
    Returns:
        float: Normalized Basel AML score
    """
    return (risk_details.basel_score_e1 + risk_details.basel_score_e2 + 
            risk_details.basel_score_intermediary) * 0.1 / 3


def country_norm(risk_details):
    """Normalize country risk factors (FATF, corruption, Basel AML).
    
    Args:
        risk_details: RiskDetails object
        
    Returns:
        float: Normalized country risk score
    """
    return (fatf_norm(risk_details) + corruption_norm(risk_details) + basel_norm(risk_details)) / 3


def persons_norm(persons):
    """Normalize PEP risk for a list of persons.
    
    Args:
        persons: List of person names
        
    Returns:
        float: Normalized PEP risk score
    """
    if len(persons) == 0:
        return 0.0
    try:
        # Prepare the JSON payload with the persons array
        payload = {"strings": persons}
        
        # Make a POST request to the specified URL with the JSON payload
        response = requests.get(
            "https://d0a3-35-196-255-153.ngrok-free.app/persons",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            # Convert the response text to float and return it
            return float(response.text)
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return 0.0
    except Exception as e:
        print(f"Error making API request: {str(e)}")
        return 0.0

def entities_norm(entities):
    """Normalize sanctioned entity risk for a list of entities.
    
    Args:
        entities: List of entity names
        
    Returns:
        float: Normalized sanctioned entity risk score
    """
    if len(entities) == 0:
        return 0.0
    try:
        # Prepare the JSON payload with the persons array
        payload = {"strings": entities}
        
        # Make a POST request to the specified URL with the JSON payload
        response = requests.get(
            "https://d0a3-35-196-255-153.ngrok-free.app/entities",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            # Convert the response text to float and return it
            return float(response.text)
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return 0.0
    except Exception as e:
        print(f"Error making API request: {str(e)}")
        return 0.0


def sanctions_norm(persons, entities):
    """Normalize sanctions risk (PEPs and sanctioned entities).
    
    Args:
        persons: List of person names
        entities: List of entity names
        
    Returns:
        float: Normalized sanctions risk score
    """
    persons_score = persons_norm(persons)
    entities_score = entities_norm(entities)
    if persons_score != 0 and entities_score != 0:
        return (persons_score + entities_score) / 2
    elif persons_score != 0:
        return persons_score
    elif entities_score != 0:
        return entities_score
    else:
        return 0


def amount_norm(amount, risky_entity):
    """Normalize transaction amount risk.
    
    Args:
        amount: Transaction amount
        risky_entity: Flag indicating if any entity is high-risk (1 or 0)
        
    Returns:
        float: Normalized transaction amount risk score
    """
    if risky_entity == 1 and amount > 10000:
        return 1
    return 0


def risk_score(country1, country2, intermediary, e1, e2, e_intermediary, persons, entities, amount, risky_entity):
    """Calculate the overall risk score for a transaction.
    
    Args:
        country1: First country name
        country2: Second country name
        intermediary: Intermediary country name
        e1: First entity name
        e2: Second entity name
        e_intermediary: Intermediary entity name
        persons: List of person names involved
        entities: List of entity names involved
        amount: Transaction amount
        risky_entity: Flag indicating if any entity is in a high-risk industry (1 or 0)
        
    Returns:
        float: Overall risk score
    """
    # Define weights for different risk factors
    weights = {
        "country": 0.2,     # FATF, corruption, Basel AML
        "transaction": 0.2,  # Transaction amount
        "sanctions": 0.2,    # Sanctioned entities, PEPs
        "industry": 0.4      # High-risk industry
    }
    # Initialize risk details object
    risk_details = RiskDetails()
    
    # Set risk factors
    set_fatf(risk_details, country1, country2, intermediary)
    set_fatf_hist(risk_details, country1, country2, intermediary)
    set_sanctioned_entity_val(risk_details, e1, e2, e_intermediary)
    set_corruption_rank(risk_details, country1, country2, intermediary)
    set_basel_score(risk_details, country1, country2, intermediary)
    # Calculate overall risk score
    score = (weights['country'] * country_norm(risk_details) + 
             weights["sanctions"] * sanctions_norm(persons, entities) + 
             weights["transaction"] * amount_norm(amount, risky_entity) + 
             weights["industry"] * risky_entity)
    
    # Calculate confidence score
    confidence_score = getConfidenceScore(risk_details)
    
    # Build output
    output = {
        'score': round(score, 3),
        'confidence_score': confidence_score,
        'resources': []
    }
    
    # Add resources based on risk factors
    if country_norm(risk_details) > 0:
        output['resources'].extend(["FATF Lists", "Corruption Score", "Basel AML"])
    if sanctions_norm(persons, entities) > 0:
        output['resources'].extend(["OpenSanctions - Sanctioned Entity", "OpenSanctions - PEP"])
    
    return output


def getConfidenceScore(risk_details: RiskDetails) -> float:
    """
    Calculate confidence score based on the completeness of risk details.
    
    Args:
        risk_details: RiskDetails object containing all risk factors
        
    Returns:
        float: Confidence score between 0.5 and 1
    """
    # List of all attributes to check
    attributes = [
        'curr_fatf_e1', 'curr_fatf_e2', 'curr_fatf_intermediary',
        'hist_fatf_e1', 'hist_fatf_e2', 'hist_fatf_intermediary',
        'sanct_entity_e1', 'sanct_entity_e2', 'sanct_entity_intermediary',
        'corruption_score_e1', 'corruption_score_e2', 'corruption_score_intermediary',
        'high_risk_industry',
        'basel_score_e1', 'basel_score_e2', 'basel_score_intermediary'
    ]
    
    # Count non-zero values
    filled_count = sum(getattr(risk_details, attr) != 0 for attr in attributes)
    
    # Calculate base confidence (scaled to 0.5-1 range)
    total_attributes = len(attributes)
    base_confidence = 0.5 + (filled_count / total_attributes) * 0.5  # Scales from 0.5 to 1
    
    # Adjust confidence based on critical factors
    critical_factors = [
        'curr_fatf_e1', 'curr_fatf_e2',
        'corruption_score_e1', 'corruption_score_e2',
        'basel_score_e1', 'basel_score_e2'
    ]
    
    critical_filled = sum(getattr(risk_details, attr) != 0 for attr in critical_factors)
    critical_weight = 0.1  # Weight for critical factors (scaled down since base is higher)
    
    confidence = base_confidence + (critical_filled / len(critical_factors)) * critical_weight
    
    confidence = min(max(confidence, 0.5), 1)
    
    return round(confidence, 3)


def process(transaction:Transaction):
    response={}
    country1 = transaction.country1
    country2 = transaction.country2
    country_intermediary = transaction.intermediary
    e1 = transaction.e1
    e2 = transaction.e2
    e_intermediary = transaction.e_intermediary
    persons = transaction.persons
    entities = transaction.entities
    jurisdictions = transaction.jurisdictions
    amount = transaction.amount
    risky_entity = transaction.risky_entity
    response = risk_score(
                country1, country2, country_intermediary,
                e1, e2, e_intermediary,
                persons, entities,
                amount, risky_entity
            )
    
    return response


if __name__ == "__main__":
    print(entities_norm(['Streloy','Wells Fargo','Sberbank']))