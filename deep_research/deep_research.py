import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)


async def run_research_with_progress(query: str):
    """Run research and yield progress updates for Gradio streaming."""
    if not query.strip():
        yield "⚠️ Please enter a research query to get started."
        return
    
    research_manager = ResearchManager()
    
    # Accumulate the output for streaming
    accumulated_output = ""
    
    async for chunk in research_manager.run(query):
        accumulated_output += chunk
        yield accumulated_output


def clear_outputs():
    """Clear the outputs and reset the interface."""
    return "", ""


# Custom CSS for better styling
custom_css = """
.gradio-container {
    max-width: 1200px !important;
}

#query_textbox textarea {
    font-size: 16px !important;
}

#report_output {
    max-height: 800px;
    overflow-y: auto;
}

.progress-container {
    border: 1px solid #e1e5e9;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
}
"""

with gr.Blocks(
    theme=gr.themes.Default(primary_hue="sky", neutral_hue="slate"),
    css=custom_css,
    title="Deep Research AI"
) as ui:
    gr.Markdown(
        """
        # 🔬 Deep Research AI
        
        Conduct comprehensive research using AI agents that plan, search, and synthesize information.
        
        **How it works:**
        1. 🎯 **Planner Agent** breaks down your query into targeted searches
        2. 🔍 **Search Agent** performs multiple web searches concurrently  
        3. 📝 **Writer Agent** synthesizes findings into a comprehensive report
        """,
        elem_id="header"
    )
    
    with gr.Row():
        with gr.Column(scale=2):
            query_textbox = gr.Textbox(
                label="Research Query",
                placeholder="Enter your research question (e.g., 'Latest developments in AI safety research')",
                lines=3,
                elem_id="query_textbox"
            )
            
            with gr.Row():
                run_button = gr.Button("🚀 Start Research", variant="primary", size="lg")
                clear_button = gr.Button("🗑️ Clear", variant="secondary")
        
        with gr.Column(scale=1):
            gr.Markdown(
                """
                ### 💡 Example Queries:
                - Latest developments in quantum computing
                - Impact of climate change on agriculture
                - Current trends in renewable energy technology
                - Advances in gene therapy treatments
                - Future of autonomous vehicles
                """
            )
    
    report_output = gr.Markdown(
        label="Research Progress & Report",
        elem_id="report_output",
        value="Enter a research query above and click 'Start Research' to begin...",
        height=600
    )
    
    # Event handlers
    run_button.click(
        fn=run_research_with_progress,
        inputs=query_textbox,
        outputs=report_output,
        show_progress=True
    )
    
    query_textbox.submit(
        fn=run_research_with_progress,
        inputs=query_textbox,
        outputs=report_output,
        show_progress=True
    )
    
    clear_button.click(
        fn=clear_outputs,
        outputs=[query_textbox, report_output]
    )

if __name__ == "__main__":
    ui.launch(
        inbrowser=True,
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True
    )

