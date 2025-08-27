from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearchResults

load_dotenv()


@tool
def triple(num: float) -> float:
    """
    Triple a number.
    """
    return float(num) * 3


tools = [triple, TavilySearchResults(max_results=2)]

llm = ChatOpenAI(model="gpt-5-nano", temperature=0).bind_tools(tools)

if __name__ == "__main__":
    print(llm.invoke("What is 3 times 3?"))