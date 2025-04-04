from langgraph.graph import START, MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage

def build_graph(rag_chain):
    def rag_node(state):
        messages = state["messages"]
        question = messages[-1].content
        response = rag_chain.invoke(question)
        return {"messages": messages + [AIMessage(content=response)]}

    workflow = StateGraph(state_schema=MessagesState)
    workflow.add_node("rag", rag_node)
    workflow.add_edge(START, "rag")
    return workflow

def get_app(rag_chain, checkpoint_path="conversation_checkpoints"):
    memory = MemorySaver.from_path(checkpoint_path)
    graph = build_graph(rag_chain)
    return graph.compile(checkpointer=memory)
