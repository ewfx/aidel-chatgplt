import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()

# from google.colab import userdata
def ask_gemini(api_key, model_name, prompt):
    """
    Connects to the Gemini API, asks a question, and returns the response.

    Args:
        api_key: Your Gemini API key.
        model_name: The name of the Gemini model to use (e.g., "gemini-pro").
        prompt: The question or prompt to send to the model.

    Returns:
        The model's response as a string, or None if an error occurs.
    """
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def parse_json_response(json_str: str) -> dict:
    """
    Parse a JSON string into a Python dictionary.
    
    Args:
        json_str: JSON string to parse
        
    Returns:
        Python dictionary containing the parsed data
    """
    try:
        # Remove the backticks if they exist
        json_str = json_str.strip('`')
        json_str=json_str.strip('json')
        # Parse the JSON string
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {str(e)}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {}

# Example usage:
api_key = os.getenv("GEMINI_API_KEY")  #key to be added
 # Replace with your actual API key.
model_name = "gemini-2.0-flash"

prompt1="""
          You are an assistant which only returns a JSON with define keys, the model JSON is :
          {
            "sender_country":extract the sender's country from the transaction data that i will give,
            "reciever_country":extract the reciever's country from the transaction data that i will give,
            "jurisdictions": list of all the countries found in the given data along with sender_country and reciever_country
          }
          Strictly no abbreviations for country names, give full country name as the value.
          The transaction data:
          """
prompt2="""
                  STRICTLY RETURN A JSON AND ONLY A JSON, nothing else to be returned. Jurisdictions list must STRICTLY CONTAIN COUNTRIES< IF THERE ARE ANY CITIES, ADD THE COUNTRY IT BELONGS TO. FOr ex: if u find Frankfurt, add Germany to the list.
        """
# response = ask_gemini(api_key, model_name, prompt)
def get_country_llm(transaction: dict) -> dict:
    return parse_json_response(ask_gemini(api_key, model_name, prompt1+str(transaction['Sender'])+str(transaction['Receiver'])+str(transaction["Proper Noun Entities"])+prompt2))

    # print(data)