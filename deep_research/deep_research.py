import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager
import asyncio

load_dotenv(override=True)

async def run_research_with_progress(query: str):
    """Run research and yield progress updates for Gradio streaming."""
    if not query.strip():
        yield "⚠️ Please enter a research query to get started."
        return
    
    research_manager = ResearchManager()
    
    # Stream all the progress updates directly
    async for output in research_manager.run(query):
        yield output

def clear_outputs():
    """Clear the outputs and reset the interface."""
    return "", ""

# Custom CSS for better styling
custom_css = """
.gradio-container {
    max-width: 1400px !important;
}

#query_textbox textarea {
    font-size: 16px !important;
}

#report_output {
    max-height: 800px;
    overflow-y: auto;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.6;
}

.progress-container {
    border: 1px solid #e1e5e9;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
}

/* Enhance markdown rendering */
#report_output h1, #report_output h2, #report_output h3 {
    color: #1f2937;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

#report_output p {
    margin-bottom: 1em;
}

#report_output ul, #report_output ol {
    margin-bottom: 1em;
    padding-left: 1.5em;
}

#report_output code {
    background-color: #f3f4f6;
    padding: 0.125em 0.25em;
    border-radius: 0.25em;
    font-size: 0.875em;
}

#report_output blockquote {
    border-left: 4px solid #3b82f6;
    padding-left: 1em;
    margin: 1em 0;
    font-style: italic;
    background-color: #f8fafc;
}

/* Status indicators */
.status-planning { color: #f59e0b; }
.status-searching { color: #3b82f6; }
.status-writing { color: #10b981; }
.status-complete { color: #059669; }
.status-error { color: #ef4444; }

/* Loading animation */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.loading {
    animation: pulse 2s infinite;
}
"""

with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="blue", neutral_hue="slate"),
    css=custom_css,
    title="Deep Research AI"
) as ui:
    # Top row: Header and Example Queries side by side
    # with gr.Row():
    #     with gr.Column(scale=3):
    #         gr.Markdown(
    #             """
    #             # 🔬 Deep Research AI
                
    #             Conduct comprehensive research using AI agents that plan, search, and synthesize information in real-time.
                
    #             **How it works:**
    #             1. 🎯 **Planner Agent** breaks down your query into targeted searches
    #             2. 🔍 **Search Agent** performs multiple web searches concurrently  
    #             3. 📝 **Writer Agent** synthesizes findings into a comprehensive report
                
    #             **✨ Watch the agents work in real-time as they collaborate to research your topic!**
    #             """,
    #             elem_id="header"
    #         )
        
    #     with gr.Column(scale=2):
    #         gr.Markdown(
    #             """
    #             ### 💡 Example Queries:
                
    #             **Technology & Science:**
    #             - Latest developments in quantum computing
    #             - Advances in gene therapy treatments
    #             - Current trends in renewable energy technology
                
    #             **Business & Economics:**
    #             - Impact of AI on job markets
    #             - Cryptocurrency regulation trends
    #             - Supply chain innovations post-COVID
                
    #             **Environment & Society:**
    #             - Climate change adaptation strategies
    #             - Urban planning for sustainable cities
    #             - Mental health tech solutions
                
    #             ### 📊 What You'll See:
    #             - **Real-time agent activity** as they plan and execute searches
    #             - **Progress tracking** for each search operation
    #             - **Live synthesis** as the report is being written
    #             - **Comprehensive final report** with insights and sources
    #             """
    #         )
    
    # Input row: Query textbox and buttons
    with gr.Row():
        with gr.Column():
            query_textbox = gr.Textbox(
                label="🔍 Research Query",
                placeholder="Enter your research question (e.g., 'Latest developments in AI safety research')",
                lines=3,
                elem_id="query_textbox"
            )
            
            with gr.Row():
                run_button = gr.Button(
                    "🚀 Start Research", 
                    variant="primary", 
                    size="lg",
                    scale=2
                )
                clear_button = gr.Button(
                    "🗑️ Clear", 
                    variant="secondary",
                    scale=1
                )
    
    # Results row: Report output
    with gr.Row():
        report_output = gr.Markdown(
            label="📈 Research Progress & Report",
            elem_id="report_output",
            value="""
            ### 👋 Welcome to Deep Research AI!            
            You'll see real-time updates as our agents:
            - 🎯 Plan targeted searches for your topic
            - 🔍 Execute multiple web searches concurrently
            - 📝 Synthesize findings into a comprehensive report
            """,
            height=700
        )
    
    # Status indicator
    with gr.Row():
        status_text = gr.Markdown(
            "**Status:** Ready to start research",
            elem_id="status_indicator"
        )
    
    # Event handlers with improved UX
    def update_status_running():
        return "**Status:** 🔄 Research in progress... (This may take 1-3 minutes)"
    
    def update_status_ready():
        return "**Status:** ✅ Ready to start new research"
    
    # Research button click
    run_button.click(
        fn=lambda: update_status_running(),
        outputs=status_text,
        queue=False
    ).then(
        fn=run_research_with_progress,
        inputs=query_textbox,
        outputs=report_output,
        show_progress=True
    ).then(
        fn=lambda: update_status_ready(),
        outputs=status_text,
        queue=False
    )
    
    # Enter key in textbox
    query_textbox.submit(
        fn=lambda: update_status_running(),
        outputs=status_text,
        queue=False
    ).then(
        fn=run_research_with_progress,
        inputs=query_textbox,
        outputs=report_output,
        show_progress=True
    ).then(
        fn=lambda: update_status_ready(),
        outputs=status_text,
        queue=False
    )
    
    # Clear button
    clear_button.click(
        fn=clear_outputs,
        outputs=[query_textbox, report_output]
    ).then(
        fn=lambda: update_status_ready(),
        outputs=status_text,
        queue=False
    )

if __name__ == "__main__":
    print("🚀 Starting Deep Research AI Interface...")
    print("📊 Features: Real-time agent progress, concurrent searches, comprehensive reports")
    print("🔗 Access your research interface at: http://127.0.0.1:7860")
    
    ui.launch(
        inbrowser=True,
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
        quiet=False
    )