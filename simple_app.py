"""
Simplified Streamlit app to test basic functionality.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Simple AI Test",
    page_icon="🧪",
    layout="wide"
)

st.title("Simple AI Test")
st.write("This is a simplified app to test if the basic AI functionality works.")

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY not found in environment variables.")
    st.stop()

# Initialize the model
@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        temperature=0.7,
        google_api_key=api_key,
        convert_system_message_to_human=True
    )

# Input form
with st.form("simple_form"):
    prompt = st.text_area("Enter your prompt:", value="Write a short paragraph about AI.")
    submit = st.form_submit_button("Generate")

# Generate content
if submit:
    with st.status("Generating content..."):
        try:
            llm = get_llm()
            messages = [HumanMessage(content=prompt)]
            
            # Debug info
            st.write("Sending request to Gemini...")
            
            # Generate response
            response = llm.invoke(messages)
            
            # Display response
            st.write("Response received!")
            
            # Show the content
            st.subheader("Generated Content:")
            st.markdown(response.content)
            
        except Exception as e:
            st.error(f"Error generating content: {e}")
            import traceback
            st.code(traceback.format_exc())
