import streamlit as st
import time
from agent_brain import app

st.set_page_config(page_title="Lex-Agentic | AI Auditor", page_icon="⚖️", layout="wide")

# Custom Styling for that "Enterprise" look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Lex-Agentic Contract Auditor")
st.caption("AI-Powered Compliance with Human-in-the-Loop Oversight")

# --- Sidebar: Observability & Status ---
with st.sidebar:
    st.header("🛠️ System Status")
    st.success("Privacy: Local PII Redaction Active")
    st.success("Memory: Qdrant Vector Store Connected")
    st.info("Observability: LangSmith Tracing On")
    
    if st.button("Clear Session"):
        st.session_state.clear()
        st.rerun()

# --- Main UI Logic ---
if "step" not in st.session_state:
    st.session_state.step = "input"

# Step 1: Input Contract
if st.session_state.step == "input":
    contract_text = st.text_area("Paste the contract text below to begin the audit:", height=300, placeholder="Enter legal text here...")
    
    if st.button("Initiate Agentic Audit"):
        if contract_text:
            st.session_state.raw_contract = contract_text
            st.session_state.step = "processing"
            st.rerun()
        else:
            st.warning("Please enter some text first.")

# Step 2: Processing & Interrupt Handling
elif st.session_state.step == "processing":
    st.header("🕵️ Agentic Reasoning in Progress")
    
    # We use a unique thread_id for this specific user session
    config = {"configurable": {"thread_id": "streamlit_user_1"}}
    inputs = {"raw_contract": st.session_state.raw_contract}
    
    with st.status("Agents working...", expanded=True) as status:
        # We run the graph. It will stop at the 'auditor' node because of interrupt_before
        for event in app.stream(inputs, config):
            st.write(event)
        status.update(label="Audit Paused: Human Review Required", state="complete")
    
    st.divider()
    st.subheader("📝 Review Research Findings")
    st.write("The AI has gathered legal precedents. Review them before proceeding to the final Audit.")
    
    # Get the current state to show research notes
    current_state = app.get_state(config)
    st.info(current_state.values.get("research_notes", "No research notes found."))

    if st.button("Approve & Generate Final Audit"):
        # Resume the graph by passing None as input for the next step
        with st.spinner("Generating final report..."):
            for event in app.stream(None, config):
                st.write(event)
            
            final_state = app.get_state(config)
            st.session_state.audit_report = final_state.values.get("audit_report")
            st.session_state.step = "final"
            st.rerun()

# Step 3: Final Report
elif st.session_state.step == "final":
    st.header("📊 Final Audit Report")
    st.markdown(st.session_state.audit_report)
    
    if st.button("Start New Audit"):
        st.session_state.step = "input"
        st.rerun()