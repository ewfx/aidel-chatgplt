from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool, serper_search_tool, scrape_tool
from dotenv import load_dotenv

import os
load_dotenv(override=True)

class ResearchResponse(BaseModel):
    company_background: str
    risk_factors: str
    additional_insights: str
    sources: list[str]
    

# llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
# llm = ChatOpenAI(model="gpt-4o-mini")
#  gemini-1.5-pro"
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/gen-lang-client-0755214413-cfc280c49d77.json"
llm = ChatVertexAI(model="gemini-1.5-flash-001", convert_system_message_to_human=True)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            "You are a research agent specialized in financial risk analysis. Your task is to gather comprehensive "
            "and reliable information about the entity in the query that is involved in a transaction. "
            Answer the user query and use neccessary tools. 
            If the entity name is abbreviated or typo is there then correct it and use full name for search queries especially for corporations
            "First, use the GoogleSearch tool to identify reputable sources, then use the WebScraper tool to extract summarized"
            "content important for analysis from the most 3 relevant websites which are webpages not pdf or any files. See the url to make this judgement.
            Avoid scraping from https://www.opensanctions.org, while scraping if you get 'No content found' scrape the next till you find 
            3 webpages to get legit information. Dont do more than 3 successful crawls per query and max 5 crawls if 'No content found' is encountered.
            Which ever url was not abled to be parsed can be added additional resource in the report.
            Also use the WikiSearch tool to gather additional information about the entity."            
            Finally, compile all findings into a well-structured markdown report "
            "with the following sections: \n\n"
            "1. **Company Background**\n"
            "2. **Risk Factors**\n"
            "3. **Additional Insights**\n" 
            "4. **Sources/Citations**\n"
            "Include citations or source notes as needed. Craft your search query appropriately to extract the best available information."
            On the research if you feel the entity is fake mention it in the report - this is very important to be mentioned if applicable
            Save to the file if the user mentions it
            Without json word in the output, just give the object back
            And Wrap the output in this format and provide no other text\n{format_instructions}             
            """
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [serper_search_tool, wiki_tool, scrape_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What can i help you research? ")
raw_response = agent_executor.invoke({"query": query})

try:
    structured_response = parser.parse(raw_response.get("output"))
    print(structured_response)
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_response)


def invoke_research_agent(query: str):
    raw_response = agent_executor.invoke({"query": query})

    try:
        structured_response = parser.parse(raw_response.get("output"))
        return (raw_response.get("output"))
    except Exception as e:
        return ("Error parsing response", e, "Raw Response - ", raw_response)