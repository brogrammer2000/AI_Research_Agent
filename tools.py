from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime


#duckduckgo search
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name = "Search_the_web",
    func = search.run,
    description = "Use this to search the web for information"
)

#wikipedia search
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=50)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

#custom tool
#defining the fuunction
def save_to_text(data: str, filename: str = "research_output,txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    formatted_text = f"--- Research Output {timestamp} ---\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    return f"Saved to {filename}"
#creating the tool
save_tool = Tool(
    name = "Save_text_to_file",
    func=save_to_text,
    description="Use this to save text to a file"
)

