from langgraph.graph import StateGraph
from typing import TypedDict, List

class IacState(TypedDict):
    query: str
    context: List
    output: str