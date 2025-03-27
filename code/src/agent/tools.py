from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
import os
import requests
import json
# Install with pip install firecrawl-py
from firecrawl import FirecrawlApp
from groq import Groq

from dotenv import load_dotenv

load_dotenv(override=True)

def save_to_txt(data: str, filename: str = "research_output.md"):
    print("inside")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)

def serper_search(query: str) -> str:
    """
    Uses the serper.dev API to perform a Google search.
    """
    url = "https://google.serper.dev/search"

    payload = json.dumps({
    "q": query,
    })
    headers = {
    'X-API-KEY': os.getenv('SERPERDEV_API_KEY'),
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        # For simplicity, we convert the response to a string.
        return f"Serper Search Results:\n{data}"
    else:
        return f"Error during serper search: {response.status_code} {response.text}"

# Wrap these functions in LangChain Tool objects.
serper_search_tool = Tool(
    name="GoogleSearch",
    func=serper_search,
    description=("Useful for conducting a Google search using the serper.dev API. "
                 "Input should be a well-crafted query to retrieve financial and background information about an entity.")
)


def firecrawl_scrape(url: str) -> str:
    """
    Uses the firecrawl API to scrape content from a given website.
    """  

    API_KEY = "YOUR_FIRECRAWL_API_KEY"  # Replace with your firecrawl API key

    app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

    try:
        response = app.scrape_url(url=url, params={
            'formats': [ 'markdown' ],
        })
        return f"Scraped Content:\n{response.get('markdown', 'No content found')}"
    except Exception as e:
        return f"Error during firecrawl scrape: {str(e)} - No content found"
    
scrape_tool = Tool(
    name="WebScraper",
    func=firecrawl_scrape,
    description=("Useful for scraping the full content of a webpage using the firecrawl API. "
                 "Input should be a URL from which detailed information is needed.")
)


search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=5, doc_content_chars_max=10000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)



def invoke_groq_cloud(research_object: str)-> str:
       
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    client = Groq(
        api_key=GROQ_API_KEY,
    )

 

    system_prompt = """
                    You are an excellent financial analyst. You must strictly base your response on the provided research content and not invent any details beyond it. Analyze the content to determine the riskiness of the transaction in the 'Raw Transaction' property. Your output must be a single JSON object with the following keys:
                - "justification": Provide a concise explanation of the risk assessment using direct evidence from the research.
                - "evidence": List one or more URLs from the research content that support your justification.
                - "entity_names": The name of the entity involved. This will be array
                - "entity_types": The type of entity (e.g., corporation, individual). This will be array corresponding enity_names
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

invoke_groq_cloud()