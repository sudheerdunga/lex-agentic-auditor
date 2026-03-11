import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from redactor import LegalRedactor
from research_storage import LegalKnowledgeBase
from dotenv import load_dotenv

load_dotenv()

# 1. Define the "State" (What the AI remembers during the task)
class AgentState(TypedDict):
    raw_contract: str
    redacted_text: str
    research_notes: str
    audit_report: str
    iterations: int

# 2. Define the Nodes (The "Workstations")
def redact_node(state: AgentState):
    print("--- STEP 1: REDACTING PII ---")
    redactor = LegalRedactor()
    safe_text = redactor.redact_contract(state["raw_contract"])
    return {"redacted_text": safe_text, "iterations": 0}

def research_node(state: AgentState):
    print("--- STEP 2: RESEARCHING PRECEDENTS ---")
    kb = LegalKnowledgeBase()
    # Search for the top 2 matching legal clauses
    results = kb.search(state["redacted_text"], limit=2)
    notes = "\n".join([r.page_content for r in results])
    return {"research_notes": notes}

def audit_node(state: AgentState):
    print("--- STEP 3: AUDITING CONTRACT ---")
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = f"""
    Compare this Contract to our Gold Standard.
    Contract: {state['redacted_text']}
    Gold Standard: {state['research_notes']}
    
    List any risks or missing clauses.
    """
    response = llm.invoke(prompt)
    return {"audit_report": response.content, "iterations": state["iterations"] + 1}

# 3. Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("redactor", redact_node)
workflow.add_node("researcher", research_node)
workflow.add_node("auditor", audit_node)

workflow.add_edge(START, "redactor")
workflow.add_edge("redactor", "researcher")
workflow.add_edge("researcher", "auditor")
workflow.add_edge("auditor", END)

# Compile
app = workflow.compile()

# Test the full Agentic Pipeline
if __name__ == "__main__":
    test_contract = "This deal is between Vijay Mallya and the Bank of India for 500 Crores."
    inputs = {"raw_contract": test_contract}
    
    for output in app.stream(inputs):
        print(output)