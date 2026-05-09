from langgraph.graph import StateGraph
from typing import TypedDict, List
from backend.rag.retriever import retrieve
from langchain_ollama import ChatOllama
from backend.config import model


class IacState(TypedDict):
    query: str
    context: List
    output: str


graph = StateGraph(IacState)


def callRag(state):
    query = state["query"]
    retrieved_data = retrieve(query)
    return {"context": retrieved_data}


def generate(state):
    llm = ChatOllama(model=model)
    query = state["query"]
    context = state["context"]
    context_text = "\n".join([doc.page_content for doc in context])
    prompt_text = f"You are a terraform expert use this context:  {context_text} and user asked for this: {query}"
    generated_code = llm.invoke(prompt_text).content
    return {"output": generated_code}


graph.add_node("knowledgebase", callRag)
graph.add_node("generator", generate)
graph.add_edge("knowledgebase", "generator")
graph.set_entry_point("knowledgebase")
graph.set_finish_point("generator")
app = graph.compile()
