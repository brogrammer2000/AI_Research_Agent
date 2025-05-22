from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool,save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    toolsUsed: list[str]

llm = ChatOpenAI(model="gpt-4o-nano")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     """
     You are a helpful assistant that will help me with my research.
     Use the search tool to find information about the user's query.
     Format your response according to these fields:
     - topic: The main subject of the research
     - summary: A comprehensive summary of the findings
     - sources: List of sources used
     - toolsUsed: List of tools used in the research
     
     {format_instructions}
     """
     ),
     ("placeholder", "{chat_history}"),
     ("human", "{query}"),
     ("placeholder", "{agent_scratchpad}")
]).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(llm = llm, tools = tools, prompt = prompt)
agent_executor = AgentExecutor(agent = agent, tools = tools)

query = input("What can I help you research?")
raw_response = agent_executor.invoke({"query": query})


try:
    structured_response = parser.parse(raw_response.get("output"))
    print(structured_response)
except Exception as e:
    print(f"Error: {e}")
    print(raw_response.get("output"))
