from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal, Annotated
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import operator

load_dotenv()

model = ChatGroq(model="llama3-8b-8192")

generator_llm = model
evaluator_llm = model
optimizer_llm = model


# structured output
class TweetEvaluation(BaseModel):
    evaluation: Literal["approved", "needs_improvement"]
    feedback: str

structured_evaluator = evaluator_llm.with_structured_output(TweetEvaluation)


# state
class TweetState(TypedDict):
    topic: str
    tweet: str
    evaluation: Literal["approved", "needs_improvement"]
    feedback: str
    iteration: int
    max_iteration: int

    tweet_history: Annotated[list[str], operator.add]
    feedback_history: Annotated[list[str], operator.add]


# generate tweet
def generate_tweet(s: TweetState):

    prompt = f"""
Write a funny, viral tweet on: {s['topic']}
- max 280 chars
- no Q&A format
- use sarcasm, memes, relatability
"""

    response = generator_llm.invoke(prompt).content

    return {"tweet": response, "tweet_history": [response]}


# evaluate tweet
def evaluate_tweet(s: TweetState):

    prompt = f"""
Evaluate this tweet:

{ s['tweet'] }

Return:
- evaluation: approved / needs_improvement
- feedback: explanation
"""

    result = structured_evaluator.invoke(prompt)

    return {
        "evaluation": result.evaluation,
        "feedback": result.feedback,
        "feedback_history": [result.feedback]
    }


# optimize tweet
def optimize_tweet(s: TweetState):

    prompt = f"""
Improve this tweet based on feedback:

Feedback: {s['feedback']}
Tweet: {s['tweet']}

Keep it viral and under 280 chars.
"""

    response = optimizer_llm.invoke(prompt).content
    return {
        "tweet": response,
        "iteration": s["iteration"] + 1,
        "tweet_history": [response]
    }


# routing
def route(s: TweetState):
    if s["evaluation"] == "approved" or s["iteration"] >= s["max_iteration"]:
        return "approved"
    return "needs_improvement"


# graph
g = StateGraph(TweetState)

g.add_node("generate", generate_tweet)
g.add_node("evaluate", evaluate_tweet)
g.add_node("optimize", optimize_tweet)

g.add_edge(START, "generate")
g.add_edge("generate", "evaluate")

g.add_conditional_edges(
    "evaluate",
    route,
    {"approved": END, "needs_improvement": "optimize"}
)

g.add_edge("optimize", "evaluate")

app = g.compile()


# run
initial_state = {
    "topic": "college life struggles",
    "iteration": 1,
    "max_iteration": 5
}

result = app.invoke(initial_state)
print(result)
