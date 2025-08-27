from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState, StateGraph, START, END
from nodes import run_agent_messages, tool_node
import os


load_dotenv()

AGENT_REASON = "agent_reason"
ACT = "act"
LAST = -1

def should_continue(state: MessagesState) -> str:
    """
    Check if the last message is a tool call.
    """

    if not state["messages"][LAST].tool_calls:
        return END
    else:
        return ACT



flow  = StateGraph(MessagesState)

flow.add_node(AGENT_REASON, run_agent_messages)
flow.set_entry_point(AGENT_REASON)
flow.add_node(ACT, tool_node)

flow.add_conditional_edges(AGENT_REASON,should_continue, {
    END: END,
    ACT: ACT
    })
flow.add_edge(ACT, AGENT_REASON)

app = flow.compile()
app.get_graph().draw_mermaid_png(output_file_path="flow.png")




if __name__ == "__main__":
    print("Starting the application react function calling with langgraph")
    res = app.invoke({"messages": [HumanMessage("What is the temperature in Tokyo today? list it and triple it")]})
    print(res["messages"][LAST].content)
