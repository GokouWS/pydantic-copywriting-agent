"""
Simplified test for the LangGraph workflow.
"""

import os
import streamlit as st
from typing import Dict, List, TypedDict, Optional, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Define a simple state
class SimpleState(TypedDict):
    prompt: str
    content: Optional[str]
    status: str
    error: Optional[str]

# Define node functions
def generate_content(state: SimpleState) -> Dict[str, Any]:
    """Generate content using the AI model."""
    print(f"Generating content for prompt: {state['prompt'][:50]}...")
    
    try:
        # Get API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return {
                "content": None,
                "status": "failed",
                "error": "GOOGLE_API_KEY not found in environment variables"
            }
        
        # Initialize the model
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0.7,
            google_api_key=api_key,
            convert_system_message_to_human=True
        )
        
        # Create message
        messages = [HumanMessage(content=state["prompt"])]
        
        # Generate response
        response = llm.invoke(messages)
        
        return {
            "content": response.content,
            "status": "completed"
        }
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print(traceback.format_exc())
        return {
            "content": None,
            "status": "failed",
            "error": str(e)
        }

# Build the graph
def build_workflow():
    """Build a simple workflow graph."""
    workflow = StateGraph(SimpleState)
    
    # Add node
    workflow.add_node("generate", generate_content)
    
    # Set entry point
    workflow.set_entry_point("generate")
    
    # Add edge to end
    workflow.add_edge("generate", END)
    
    # Compile the graph
    return workflow.compile()

# Streamlit app
st.title("Simple LangGraph Test")
st.write("This is a simplified app to test if the LangGraph workflow works.")

# Input form
with st.form("simple_graph_form"):
    prompt = st.text_area("Enter your prompt:", value="Write a short paragraph about AI.")
    submit = st.form_submit_button("Generate with LangGraph")

# Generate content
if submit:
    with st.status("Generating content with LangGraph..."):
        try:
            # Initialize the state
            initial_state = SimpleState(
                prompt=prompt,
                content=None,
                status="initialized",
                error=None
            )
            
            # Build and run the workflow
            workflow = build_workflow()
            st.write("Workflow built, running...")
            
            # Execute the workflow
            final_state = workflow.invoke(initial_state)
            st.write(f"Workflow completed with status: {final_state['status']}")
            
            # Show the content
            if final_state.get("content"):
                st.subheader("Generated Content:")
                st.markdown(final_state["content"])
            else:
                st.error(f"No content generated. Error: {final_state.get('error', 'Unknown error')}")
            
        except Exception as e:
            st.error(f"Error in workflow: {e}")
            import traceback
            st.code(traceback.format_exc())
