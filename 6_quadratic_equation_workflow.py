from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal

class QuadState(TypedDict):
    a: int
    b: int
    c: int
    discriminant: float
    result: str

def calc_d(state: QuadState):
    state["discriminant"] = state["b"]**2 - 4*state["a"]*state["c"]
    return state

def real_roots(state: QuadState):
    d = state["discriminant"]
    a, b = state["a"], state["b"]
    r1 = (-b + d**0.5) / (2*a)
    r2 = (-b - d**0.5) / (2*a)
    state["result"] = f"Roots: {r1}, {r2}"
    return state

def repeated_root(state: QuadState):
    a, b = state["a"], state["b"]
    state["result"] = f"Repeated root: {-b/(2*a)}"
    return state

def no_real(state: QuadState):
    state["result"] = "No real roots"
    return state

def router(state: QuadState) -> Literal["real", "repeat", "none"]:
    d = state["discriminant"]
    if d > 0:
        return "real"
    elif d == 0:
        return "repeat"
    else:
        return "none"

graph = StateGraph(QuadState)

graph.add_node("calc_d", calc_d)
graph.add_node("real", real_roots)
graph.add_node("repeat", repeated_root)
graph.add_node("none", no_real)

graph.add_edge(START, "calc_d")
graph.add_conditional_edges("calc_d", router)

graph.add_edge("real", END)
graph.add_edge("repeat", END)
graph.add_edge("none", END)

workflow = graph.compile()

graph_image = workflow.get_graph().draw_mermaid_png()
with open("quad_graph.png", "wb") as f:
    f.write(graph_image)

print(workflow.invoke({
    "a": 2,
    "b": 4,
    "c": 2
}))
