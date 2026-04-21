from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model="llama3-8b-8192")


class State(TypedDict):
    q: str
    a: str


def ask(s: State):
    s["a"] = model.invoke(s["q"]).content
    return s


g = StateGraph(State)

g.add_node("ask", ask)

g.add_edge(START, "ask")
g.add_edge("ask", END)

app = g.compile()


print(app.invoke({"q": "What is the capital of India?"})["a"])
