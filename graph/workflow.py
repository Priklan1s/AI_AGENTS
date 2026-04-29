from langgraph.graph import StateGraph, END
from typing import TypedDict

from agents.requirement_agent import requirement_agent
from agents.risk_agent import risk_agent
from agents.test_design_agent import test_design_agent
from agents.testcase_agent import testcase_agent
from agents.reviewer_agent import reviewer_agent


class State(TypedDict):

    requirements: str
    analysis: str
    risks: str
    test_design: str
    testcases: str
    review: str


builder = StateGraph(State)

builder.add_node("analyze_requirements", requirement_agent)
builder.add_node("risk_analysis", risk_agent)
builder.add_node("test_design", test_design_agent)
builder.add_node("generate_testcases", testcase_agent)
builder.add_node("review_testcases", reviewer_agent)


builder.set_entry_point("analyze_requirements")

builder.add_edge("analyze_requirements", "risk_analysis")
builder.add_edge("risk_analysis", "test_design")
builder.add_edge("test_design", "generate_testcases")
builder.add_edge("generate_testcases", "review_testcases")
builder.add_edge("review_testcases", END)

graph = builder.compile()