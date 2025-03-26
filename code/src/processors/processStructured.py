"""
Structured Transaction Processor with Enhanced Data Normalization and spaCy NER Integration
"""

import os
import json
import re
import logging
from typing import Dict, List, Optional, Union
import pandas as pd
import spacy

# --- Configure Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- Load spaCy Model ---
nlp = spacy.load("en_core_web_lg")

# --- Constants ---
ABBREVIATION_MAP = {
    "corp": "corporation",
    "inc": "incorporated",
    "ltd": "limited",
    "co": "company",
    "intl": "international",
    "plc": "public limited company",
    "llc": "limited liability company",
    "gmbh": "gesellschaft mit beschränkter haftung",
    "org": "organisation"
}

ENTITY_KEYWORDS = {
    "Bank": {"bank", "finance", "nbd", "deutsche", "credit", "trust"},
    "Organization": {"ltd", "corp", "inc", "plc", "llc", "gmbh", "co", "trading", "org", "intl"},
    "Jurisdiction": {"street", "road", "district", "city", "state", "country", "island", "zone", "lane", "cross"},
    # Add keywords for person detection
    "Person": {"mr", "mrs", "ms", "dr", "miss"}
}

REQUIRED_FIELDS = [
    "Date",
    "Transaction Type",
    "Reference",
    "Sender Account",
    "Sender Address",
    "Receiver Account",
    "Receiver Address",
    "Receiver Name",
    "Amount",
    "Transaction Details"
]

# --- Precompiled Regex Patterns ---
PUNCTUATION_PATTERN = re.compile(r'[^\w\s]')
WHITESPACE_PATTERN = re.compile(r'\s+')
AMOUNT_CLEAN_PATTERN = re.compile(r'[^\d.]')

# --- Helper Functions ---


def robust_standardize(name: Optional[str], abbrev_map: Dict[str, str]) -> Optional[str]:
    """Standardizes entity names with advanced normalization."""
    if not name or not isinstance(name, str):
        return None

    # Normalization pipeline
    name = (
        name.lower()
        .strip()
        .replace('-', ' ')
    )
    name = PUNCTUATION_PATTERN.sub('', name)

    # Ordered abbreviation replacement (longest first)
    for abbr, full in sorted(abbrev_map.items(), key=lambda x: (-len(x[0]), x[0])):
        name = re.sub(rf'\b{re.escape(abbr)}\b', full, name)

    return WHITESPACE_PATTERN.sub(' ', name)


def identify_entity_type(name: Optional[str]) -> str:
    """Identifies entity type using multi-level keyword matching with spaCy fallback."""

    if not name or not isinstance(name, str):
        return "Unknown"

    lower_name = name.lower()

    # Check for jurisdiction keywords first
    if any(keyword in lower_name for keyword in ENTITY_KEYWORDS["Jurisdiction"]):
        return "Jurisdiction"

    # Check for financial institutions
    if any(keyword in lower_name for keyword in ENTITY_KEYWORDS["Bank"]):
        return "Bank"

    # Check for organizational indicators
    if any(keyword in lower_name for keyword in ENTITY_KEYWORDS["Organization"]):
        return "Organization"

    # Check for person indicators
    if any(keyword in lower_name for keyword in ENTITY_KEYWORDS["Person"]):
        return "Person"

    # Fallback to spaCy NER
    doc = nlp(name)

    for ent in doc.ents:
        if ent.label_ == 'ORG':
            return 'Organization'
        elif ent.label_ in ['GPE', 'LOC']:
            return 'Jurisdiction'
        elif ent.label_ == 'PERSON':
            return 'Person'

    # Default to Unknown if no match is found
    return 'Unknown'


def clean_amount(value: Union[str, float, int]) -> str:
    """Converts amount strings to numeric format."""

    if pd.isna(value):
        return '0'

    return AMOUNT_CLEAN_PATTERN.sub('', str(value)).strip() or '0'


def process_transaction_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Processes raw transaction DataFrame with data normalization."""

    # Column standardization
    df = df.rename(columns={
        'Transaction': 'Transaction ID',
        'Payer Name': 'Sender Name'
    }).copy()

    # Ensure required columns exist
    for col in REQUIRED_FIELDS:
        if col not in df:
            df[col] = None

    # Data cleaning pipeline
    df['Amount'] = df['Amount'].apply(clean_amount)

    df['Sender Name'] = df['Sender Name'].apply(
        lambda x: robust_standardize(x, ABBREVIATION_MAP)
    )

    df['Receiver Name'] = df['Receiver Name'].apply(
        lambda x: robust_standardize(x, ABBREVIATION_MAP)
    )

    # Process transaction notes
    df['Notes'] = df['Transaction Details'].apply(
        lambda x: [x.strip()] if pd.notna(x) and x.strip() else []
    )

    return df


def build_transaction_json(df: pd.DataFrame) -> List[Dict]:
    """Constructs structured JSON output from processed DataFrame."""

    transactions = []

    for _, row in df.iterrows():
        sender_type = identify_entity_type(row["Sender Name"])
        receiver_type = identify_entity_type(row["Receiver Name"])

        transaction_data = {
            'Raw Transaction': json.dumps(row.to_dict(), indent=2),
            'Transaction ID': row['Transaction ID'],
            'Date': row['Date'],
            'Amount': row['Amount'],
            'Transaction Type': row['Transaction Type'],
            'Reference': row['Reference'],
            'Sender': {
                'Name': row['Sender Name'],
                'Account': row['Sender Account'],
                'Jurisdiction': row['Sender Address'],
                'Additional Info': []
            },
            'Receiver': {
                'Name': row['Receiver Name'],
                'Account': row['Receiver Account'],
                'Jurisdiction': row['Receiver Address'],
                'Additional Info': []
            },
            'Transaction Details': {
                'Notes': row['Notes']
            },
            'Proper Noun Entities': [
                {'Entity Name': row['Sender Name'],
                    'Entity Type': sender_type},
                {'Entity Name': row['Receiver Name'],
                    'Entity Type': receiver_type},
                {'Entity Name': row.get(
                    'Receiver Country', ''), 'Entity Type': 'Jurisdiction'}
            ]
        }

        transactions.append(transaction_data)

    return transactions


def process_structured_transactions(csv_path: str) -> List[Dict]:
    """Main processing pipeline for transaction data."""
    try:
        df = pd.read_csv(csv_path)

        processed_df = process_transaction_dataframe(df)
        return build_transaction_json(processed_df)

    except FileNotFoundError:
        logger.error(f"Input file not found: {csv_path}")
        return []
    except pd.errors.EmptyDataError:
        logger.error("Input file is empty or corrupt")
        return []
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        return [] 