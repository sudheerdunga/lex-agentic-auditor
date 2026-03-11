import streamlit as st
from agent_brain import app # Import the graph we built

st.set_page_config(page_title="Lex-Agentic Auditor", layout="wide")
st.title("⚖️ Lex-Agentic: AI Legal Review")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for Monitoring
with st.sidebar:
    st.header("System Vitals")
    st.info("Observability: Connected to LangSmith")
    st.success("Privacy: Local Redactor Active")

# Input Area
user_input = st.text_area("Paste Legal Contract Here:", height=200)

if st.button("Start AI Audit"):
    with st.spinner("Agentic Team is reviewing..."):
        # We stream the graph steps to show progress in the UI
        config = {"configurable": {"thread_id": "1"}}
        inputs = {"raw_contract": user_input}
        
        for event in app.stream(inputs, config):
            for node, output in event.items():
                st.write(f"✅ Node **{node}** completed.")
                if "audit_report" in output:
                    st.subheader("Final Audit Findings")
                    st.markdown(output["audit_report"])