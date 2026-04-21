from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model="llama3-8b-8192")

class ReviewState(TypedDict):
    review: str
    sentiment: Literal["positive", "negative"]
    response: str

def detect_sentiment(state: ReviewState):
    prompt = f"Classify sentiment: {state['review']}"
    res = model.invoke(prompt).content.lower()

    state["sentiment"] = "positive" if "positive" in res else "negative"
    return state

def route(state: ReviewState):
    if state["sentiment"] == "positive":
        return "good"
    return "bad"

def good_response(state: ReviewState):
    state["response"] = "Thank you for your feedback ❤️"
    return state

def bad_response(state: ReviewState):
    state["response"] = "Sorry for the issue. We will fix it ASAP."
    return state

graph = StateGraph(ReviewState)

graph.add_node("detect", detect_sentiment)
graph.add_node("good", good_response)
graph.add_node("bad", bad_response)

graph.add_edge(START, "detect")

graph.add_conditional_edges("detect", route)

graph.add_edge("good", END)
graph.add_edge("bad", END)

workflow = graph.compile()

# FLOWCHART
img = workflow.get_graph().draw_mermaid_png()
with open("review_graph.png", "wb") as f:
    f.write(img)

print(workflow.invoke({
    "review": "The app is very good and useful"
}))
