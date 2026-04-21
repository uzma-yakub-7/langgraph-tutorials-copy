from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    weight: float
    height: float
    bmi: float
    category: str

def calc_bmi(s: State):
    s["bmi"] = round(s["weight"] / (s["height"] ** 2), 2)
    return s

def label(s: State):
    b = s["bmi"]
    s["category"] = (
        "Underweight" if b < 18.5 else
        "Normal" if b < 25 else
        "Overweight" if b < 30 else
        "Obese"
    )
    return s

g = StateGraph(State)
g.add_node("bmi", calc_bmi)
g.add_node("label", label)

g.add_edge(START, "bmi")
g.add_edge("bmi", "label")
g.add_edge("label", END)

app = g.compile()

print(app.invoke({"weight": 80, "height": 1.73}))
