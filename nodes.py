from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from reactagent import llm, tools

load_dotenv()

SYSTEM_PROMPT = """
You are a helpful assistant that can use the following tools to answer questions:
"""
def run_agent_messages(state: MessagesState)->MessagesState:
    """ run the agent reasing node """

    response = llm.invoke([{"role": "system", "content": SYSTEM_PROMPT}, *state["messages"]])

    return {"messages": [response]}

tool_node = ToolNode(tools)





def main():
    graph = StateGraph(llm)
    graph.add_node("tool", ToolNode(tools))
    graph.add_edge(START, "tool")
    graph.add_edge("tool", END)
    graph.compile()
    return graph