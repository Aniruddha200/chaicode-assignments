from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict
from enum import Enum 



class State(TypedDict):
    sys_msg: str
    usr_msg: str
    usr_msg_type: str
    bot_msg: str



#write the nodes
def determine_usr_msg_type(state: State):
    usr_msg = state["usr_msg"]
    if usr_msg.startswith("multi"):
        state["usr_msg_type"] = "multi_turn_conversation"
        return state
    elif usr_msg.startswith("complex"):
        state["usr_msg_type"] = "complex_conversation"
        return state
    else:
        state["usr_msg_type"] = "simple_conversation"
        return state


def process_usr_msg(state: State):
    usr_msg = state["usr_msg"]
    usr_msg_type = state["usr_msg_type"]
    if usr_msg_type == "multi_turn_conversation":
        state["bot_msg"] = "Let's break this down into smaller parts."
        return state
    elif usr_msg_type == "complex_conversation":
        state["bot_msg"] = "This is a complex topic, let's discuss it in detail."
        return state
    else:
        state["bot_msg"] = "I can help you with that. What do you need?"
        return state


graph_builder = StateGraph(State)
graph_builder.add_node(determine_usr_msg_type)
graph_builder.add_node(process_usr_msg)
graph_builder.add_edge(START, "determine_usr_msg_type")
graph_builder.add_edge("determine_usr_msg_type", "process_usr_msg")
graph_builder.add_edge("process_usr_msg", END)
graph = graph_builder.compile()
result = graph.invoke({
    "sys_msg": "Hello, how can I help you?",
    "usr_msg": "multi: I have a question about your product.",
    "usr_msg_type": "",
    "bot_msg": "Sure, what is your question?"
})

print(result)
    




