from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
import operator
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model="llama3-8b-8192")

class EvaluationSchema(BaseModel):
    feedback: str
    score: int = Field(ge=0, le=10)

structured_model = model.with_structured_output(EvaluationSchema)

class UPSCState(TypedDict):
    essay: str
    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str
    individual_scores: Annotated[list[int], operator.add]
    avg_score: float

def evaluate_language(state: UPSCState):
    res = structured_model.invoke(
        f"Evaluate language:\n{state['essay']}"
    )
    return {
        "language_feedback": res.feedback,
        "individual_scores": [res.score]
    }

def evaluate_analysis(state: UPSCState):
    res = structured_model.invoke(
        f"Evaluate analysis:\n{state['essay']}"
    )
    return {
        "analysis_feedback": res.feedback,
        "individual_scores": [res.score]
    }

def evaluate_clarity(state: UPSCState):
    res = structured_model.invoke(
        f"Evaluate clarity:\n{state['essay']}"
    )
    return {
        "clarity_feedback": res.feedback,
        "individual_scores": [res.score]
    }

def final(state: UPSCState):
    state["avg_score"] = sum(state["individual_scores"]) / len(state["individual_scores"])
    return state

graph = StateGraph(UPSCState)

graph.add_node("lang", evaluate_language)
graph.add_node("analysis", evaluate_analysis)
graph.add_node("clarity", evaluate_clarity)
graph.add_node("final", final)

graph.add_edge(START, "lang")
graph.add_edge(START, "analysis")
graph.add_edge(START, "clarity")

graph.add_edge("lang", "final")
graph.add_edge("analysis", "final")
graph.add_edge("clarity", "final")
graph.add_edge("final", END)

workflow = graph.compile()

graph_image = workflow.get_graph().draw_mermaid_png()
with open("essay_graph.png", "wb") as f:
    f.write(graph_image)

print(workflow.invoke({
    "essay": "India is growing fast in AI..."
}))
