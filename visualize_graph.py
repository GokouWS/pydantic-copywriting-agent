"""
Utility script to visualize the LangGraph workflow.
"""

import os
from graph_agent import CopywritingGraphAgent
from models import ContentRequest, ContentType, ToneType, AudienceType

def visualize_graph():
    """
    Generate and save a visualization of the LangGraph workflow.
    """
    # Create the agent
    agent = CopywritingGraphAgent()
    
    # Get the graph
    graph = agent.workflow
    
    # Visualize the graph
    try:
        # Create the visualization
        from IPython.display import display
        import graphviz
        
        # Convert to graphviz
        dot = graph.get_graph().to_graphviz()
        
        # Save the visualization
        dot.render("workflow_graph", format="png", cleanup=True)
        
        print("Graph visualization saved as 'workflow_graph.png'")
    except Exception as e:
        print(f"Error visualizing graph: {e}")
        print("You may need to install graphviz: pip install graphviz")

if __name__ == "__main__":
    visualize_graph()
