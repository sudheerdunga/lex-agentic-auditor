import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from redactor import LegalRedactor
from research_storage import LegalKnowledgeBase
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

# Load .env for OpenAI and LangSmith keys
load_dotenv()

# 1. Define the State
class AgentState(TypedDict):
    raw_contract: str
    redacted_text: str
    research_notes: str
    audit_report: str
    iterations: int

# 2. Define the Nodes
def redact_node(state: AgentState):
    print("--- STEP 1: REDACTING PII (LOCAL) ---")
    redactor = LegalRedactor()
    safe_text = redactor.redact_contract(state["raw_contract"])
    return {"redacted_text": safe_text, "iterations": 0}

def research_node(state: AgentState):
    print("--- STEP 2: RESEARCHING PRECEDENTS ---")
    kb = LegalKnowledgeBase()
    results = kb.search(state["redacted_text"], limit=2)
    notes = "\n".join([r.page_content for r in results])
    return {"research_notes": notes}

def audit_node(state: AgentState):
    print("--- STEP 3: AUDITING CONTRACT ---")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = f"""
    Compare this Contract to our Gold Standard.
    Contract: {state['redacted_text']}
    Gold Standard: {state['research_notes']}
    
    List any risks or missing clauses.
    """
    response = llm.invoke(prompt)
    return {"audit_report": response.content, "iterations": state["iterations"] + 1}

# 3. Build and Compile the Graph
workflow = StateGraph(AgentState)

workflow.add_node("redactor", redact_node)
workflow.add_node("researcher", research_node)
workflow.add_node("auditor", audit_node)

workflow.add_edge(START, "redactor")
workflow.add_edge("redactor", "researcher")
workflow.add_edge("researcher", "auditor")
workflow.add_edge("auditor", END)

# Checkpointer for Human-in-the-Loop and Observability
memory = MemorySaver()

# ONE compile to rule them all
app = workflow.compile(
    checkpointer=memory, 
    interrupt_before=["auditor"] 
)

if __name__ == "__main__":
    # In 2026, every run needs a unique thread_id for tracing
    config = {"configurable": {"thread_id": "audit_session_001"}}
    
    test_contract = "This deal is between Rajesh Kumar and the Bank of India for 500 Crores."
    inputs = {"raw_contract": test_contract}
    
    print("\n🚀 Starting Agentic Workflow...")
    for output in app.stream(inputs, config):
        print(output)
    
    print("\n⏸️  AI is now PAUSED for Human Review. (Check LangSmith for traces)")