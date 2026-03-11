import streamlit as st
import os
from agent_brain import app as agent_graph
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Lex-Agentic | AI Legal Auditor",
    page_icon="⚖️",
    layout="wide"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .stAlert { border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .report-box { background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("⚖️ Lex-Agentic v1.0")
    st.info("Status: **Production Ready**")
    st.divider()
    st.markdown("### System Architecture")
    st.write("- **Privacy:** Local PII Redaction")
    st.write("- **Memory:** Qdrant Vector DB")
    st.write("- **Orchestration:** LangGraph")
    st.divider()
    if st.button("Reset Session"):
        st.session_state.clear()
        st.rerun()

# --- Title & Description ---
st.title("AI-Powered Legal Contract Auditor")
st.write("This agent masks PII locally, researches gold-standard precedents, and identifies legal risks.")

# --- Session State Initialization ---
if "step" not in st.session_state:
    st.session_state.step = "input"
if "thread_id" not in st.session_state:
    # Use a fixed thread_id for the session to maintain LangGraph state
    st.session_state.thread_id = f"audit_{int(st.session_state.get('start_time', 0))}"

config = {"configurable": {"thread_id": st.session_state.thread_id}}

# --- Workflow Steps ---

# STEP 1: Input Contract
if st.session_state.step == "input":
    contract_input = st.text_area("Paste the Legal Contract Text:", height=300, 
                                  placeholder="E.g., This agreement is between Rajesh Kumar and Global Tech...")
    
    if st.button("Run Audit"):
        if contract_input.strip():
            st.session_state.raw_contract = contract_input
            st.session_state.step = "processing"
            st.rerun()
        else:
            st.error("Please paste a contract to begin.")

# STEP 2: Agent Processing & Interrupt
elif st.session_state.step == "processing":
    st.subheader("🕵️ Agentic Reasoning Engine")
    
    # We display a placeholder for progress
    progress_placeholder = st.empty()
    
    # Check if we already have the state (to see if research is already done)
    state_snapshot = agent_graph.get_state(config)
    
    if not state_snapshot.values:
        # Start the graph execution
        inputs = {"raw_contract": st.session_state.raw_contract}
        with st.status("Agents are collaborating...", expanded=True) as status:
            for event in agent_graph.stream(inputs, config):
                for node_name, node_output in event.items():
                    st.write(f"✅ Node **{node_name}** completed.")
            status.update(label="Research Complete - Human Review Required", state="complete")
    
    # Refresh snapshot after stream finishes (at the interrupt point)
    state_snapshot = agent_graph.get_state(config)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔒 Redacted Text (Sent to LLM)")
        redacted = state_snapshot.values.get("redacted_text", "No redaction found.")
        st.info(redacted)

    with col2:
        st.markdown("### 📚 Legal Research Notes")
        notes = state_snapshot.values.get("research_notes", "No research notes found.")
        if notes:
            st.success(notes)
        else:
            st.warning("No relevant precedents found in Knowledge Base.")

    st.divider()
    st.warning("⚠️ **Human-in-the-Loop:** Please review the research notes above. If they are correct, click the button below to generate the final Risk Audit.")
    
    if st.button("Approve & Finalize Audit"):
        with st.spinner("Agent generating final risk assessment..."):
            # Resuming the graph by passing 'None' as input
            for event in agent_graph.stream(None, config):
                st.write(f"✅ Final Node **{list(event.keys())[0]}** completed.")
            
            # Move to final view
            st.session_state.step = "final"
            st.rerun()

# STEP 3: Final Report
elif st.session_state.step == "final":
    state_snapshot = agent_graph.get_state(config)
    audit_report = state_snapshot.values.get("audit_report", "Error generating report.")
    
    st.subheader("📊 Final Legal Audit Report")
    st.markdown('<div class="report-box">', unsafe_allow_html=True)
    st.markdown(audit_report)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    if st.button("New Audit"):
        st.session_state.step = "input"
        st.rerun()