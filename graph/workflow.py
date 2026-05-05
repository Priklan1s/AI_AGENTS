from langgraph.graph import StateGraph, END

from agents.requirement_structurer import requirement_structurer
from agents.rag_agent import rag_agent
from agents.requirement_agent import requirement_agent
from agents.risk_agent import risk_agent
from agents.test_design_agent import test_design_agent
from agents.coverage_agent import coverage_agent
from agents.testcase_agent import testcase_agent
from agents.self_critic_agent import self_critic_agent


def create_graph():

    workflow = StateGraph(dict)

    workflow.add_node("structure", requirement_structurer)
    workflow.add_node("rag", rag_agent)
    workflow.add_node("analysis", requirement_agent)
    workflow.add_node("risk", risk_agent)
    workflow.add_node("design", test_design_agent)
    workflow.add_node("coverage", coverage_agent)
    workflow.add_node("testcases", testcase_agent)
    workflow.add_node("critic", self_critic_agent)

    workflow.set_entry_point("structure")

    workflow.add_edge("structure", "rag")
    workflow.add_edge("rag", "analysis")
    workflow.add_edge("analysis", "risk")
    workflow.add_edge("risk", "design")
    workflow.add_edge("design", "coverage")
    workflow.add_edge("coverage", "testcases")
    workflow.add_edge("testcases", "critic")
    workflow.add_edge("critic", END)

    return workflow.compile()


graph = create_graph()