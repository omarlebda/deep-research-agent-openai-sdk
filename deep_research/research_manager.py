from agents import Runner, trace, gen_trace_id, Agent, function_tool
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
import asyncio
from typing import List, AsyncGenerator
from pydantic import BaseModel
import threading
import queue

# Thread-safe queue for progress messages
progress_queue = queue.Queue()

def add_progress(message: str):
    """Add a progress message to the queue (thread-safe)."""
    progress_queue.put(message)

# Pydantic models for tool parameters and returns
class SearchPlan(BaseModel):
    searches: List[WebSearchItem]
    total_searches: int

# Tool Functions - properly decorated with @function_tool
@function_tool
async def plan_research_searches(query: str) -> SearchPlan:
    """Tool to plan the searches needed for a research query.
    
    Args:
        query: The research query to plan searches for
        
    Returns:
        SearchPlan containing planned searches and count
    """
    add_progress("🎯 **Planning Research Searches...**\n")
    add_progress(f"📝 Analyzing query: *{query}*\n")
    
    result = await Runner.run(planner_agent, f"Query: {query}")
    search_plan = result.final_output_as(WebSearchPlan)
    
    add_progress(f"✅ **Planning Complete!** Will perform {len(search_plan.searches)} targeted searches\n\n")
    
    # Show the planned searches
    add_progress("📋 **Planned Searches:**\n")
    for i, search in enumerate(search_plan.searches, 1):
        add_progress(f"   {i}. *{search.query}* - {search.reason}\n")
    add_progress("\n")
    
    return SearchPlan(
        searches=search_plan.searches,
        total_searches=len(search_plan.searches)
    )

@function_tool
async def perform_multiple_searches(search_plan: SearchPlan) -> List[str]:
    """Tool to perform multiple searches concurrently.
    
    Args:
        search_plan: SearchPlan object containing searches to perform
        
    Returns:
        List of search results as strings
    """
    add_progress(f"🔍 **Starting {search_plan.total_searches} Concurrent Searches...**\n\n")
    
    async def single_search(search_item: WebSearchItem, search_num: int):
        add_progress(f"🔎 Search {search_num}: *{search_item.query}*\n")
        input_text = f"Search term: {search_item.query}\nReason for searching: {search_item.reason}"
        try:
            result = await Runner.run(search_agent, input_text)
            add_progress(f"✅ Search {search_num} completed\n")
            return str(result.final_output)
        except Exception as e:
            add_progress(f"❌ Search {search_num} failed: {str(e)}\n")
            return None
    
    tasks = [asyncio.create_task(single_search(item, i+1)) for i, item in enumerate(search_plan.searches)]
    results = []
    num_completed = 0
    
    for task in asyncio.as_completed(tasks):
        result = await task
        if result is not None:
            results.append(result)
        num_completed += 1
        add_progress(f"📊 **Progress**: {num_completed}/{len(tasks)} searches completed\n")
    
    add_progress(f"🎉 **All Searches Complete!** Gathered {len(results)} successful results\n\n")
    return results

@function_tool
async def write_research_report(query: str, search_results: List[str]) -> str:
    """Tool to write a comprehensive research report.
    
    Args:
        query: The original research query
        search_results: List of search results to synthesize
        
    Returns:
        Markdown formatted research report
    """
    add_progress("📝 **Writing Comprehensive Report...**\n")
    add_progress(f"📊 Synthesizing {len(search_results)} search results\n")
    add_progress("🧠 Analyzing patterns and insights\n")
    
    input_text = f"Original query: {query}\nSummarized search results: {search_results}"
    
    result = await Runner.run(writer_agent, input_text)
    report_data = result.final_output_as(ReportData)
    
    add_progress("✅ **Report Generation Complete!**\n\n")
    add_progress("---\n\n")
    
    return report_data.markdown_report

# Research Manager Agent
research_manager_instructions = """
You are a Research Manager agent that conducts comprehensive research.

Your workflow:
1. Use plan_research_searches to plan the research for the given query - this returns a SearchPlan object
2. Use perform_multiple_searches with the SearchPlan object to execute all planned searches
3. Use write_research_report to create the final report using the original query and search results

Always follow this sequence and provide status updates to the user.
"""

research_manager = Agent(
    name="Research Manager",
    instructions=research_manager_instructions,
    tools=[plan_research_searches, perform_multiple_searches, write_research_report],
    model="gpt-4o-mini"
)

# ResearchManager Class for Gradio Interface
class ResearchManager:
    """Research Manager class that yields step-by-step progress updates."""
    
    async def run(self, query: str) -> AsyncGenerator[str, None]:
        """Run deep research on a given query with step-by-step progress updates."""
        trace_id = gen_trace_id()
        
        # Clear any existing messages in the queue
        while not progress_queue.empty():
            try:
                progress_queue.get_nowait()
            except queue.Empty:
                break
        
        accumulated_output = f"🚀 **Starting Deep Research** for query: *{query}*\n\n"
        accumulated_output += f"📊 **Trace ID**: {trace_id}\n"
        accumulated_output += f"🔗 [View trace](https://platform.openai.com/traces/trace?trace_id={trace_id})\n\n"
        yield accumulated_output
        
        with trace("Deep Research", trace_id=trace_id):
            try:
                accumulated_output += "## 🤖 Starting Research Manager Agent\n"
                accumulated_output += "⚙️ **Agent**: Research Manager is orchestrating the complete research workflow...\n\n"
                yield accumulated_output
                
                # Create a task to run the research manager
                research_task = asyncio.create_task(
                    Runner.run(research_manager, f"Conduct research on: {query}")
                )
                
                # Monitor progress while research is running
                while not research_task.done():
                    # Check for new progress messages
                    messages_this_iteration = []
                    while not progress_queue.empty():
                        try:
                            message = progress_queue.get_nowait()
                            messages_this_iteration.append(message)
                        except queue.Empty:
                            break
                    
                    if messages_this_iteration:
                        for message in messages_this_iteration:
                            accumulated_output += message
                        yield accumulated_output
                    
                    # Small delay to prevent busy waiting
                    await asyncio.sleep(0.1)
                
                # Check for any final progress messages
                while not progress_queue.empty():
                    try:
                        message = progress_queue.get_nowait()
                        accumulated_output += message
                        yield accumulated_output
                    except queue.Empty:
                        break
                
                # Get the final result
                result = await research_task
                
                accumulated_output += "# 📊 Final Research Report\n\n"
                accumulated_output += str(result.final_output)
                yield accumulated_output
                
            except Exception as e:
                accumulated_output += f"❌ **Error occurred**: {str(e)}\n\n"
                accumulated_output += "Please try again or contact support if the issue persists."
                yield accumulated_output