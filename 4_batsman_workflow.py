from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class BatsmanState(TypedDict):
    runs: int
    balls: int
    fours: int
    sixes: int
    sr: float
    bpb: float
    boundary_percent: float
    summary: str

def calculate_sr(state: BatsmanState):
    state["sr"] = (state["runs"] / state["balls"]) * 100
    return state

def calculate_bpb(state: BatsmanState):
    state["bpb"] = state["balls"] / (state["fours"] + state["sixes"])
    return state

def calculate_boundary_percent(state: BatsmanState):
    state["boundary_percent"] = (
        ((state["fours"] * 4 + state["sixes"] * 6) / state["runs"]) * 100
    )
    return state

def summary(state: BatsmanState):
    state["summary"] = f"""
Strike Rate: {state['sr']}
Balls per Boundary: {state['bpb']}
Boundary %: {state['boundary_percent']}
"""
    return state

graph = StateGraph(BatsmanState)

graph.add_node("sr", calculate_sr)
graph.add_node("bpb", calculate_bpb)
graph.add_node("bp", calculate_boundary_percent)
graph.add_node("summary", summary)

graph.add_edge(START, "sr")
graph.add_edge(START, "bpb")
graph.add_edge(START, "bp")

graph.add_edge("sr", "summary")
graph.add_edge("bpb", "summary")
graph.add_edge("bp", "summary")
graph.add_edge("summary", END)

workflow = graph.compile()

# FLOWCHART GENERATION (NO MANUAL PNG)
graph_image = workflow.get_graph().draw_mermaid_png()
with open("batsman_graph.png", "wb") as f:
    f.write(graph_image)

# RUN
print(workflow.invoke({
    "runs": 100,
    "balls": 50,
    "fours": 6,
    "sixes": 4
}))
