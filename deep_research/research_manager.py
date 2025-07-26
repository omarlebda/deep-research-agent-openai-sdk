from agents import Runner, trace, gen_trace_id, Agent, function_tool
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
import asyncio
from typing import List, AsyncGenerator
from pydantic import BaseModel

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
    print("Planning searches...")
    result = await Runner.run(planner_agent, f"Query: {query}")
    search_plan = result.final_output_as(WebSearchPlan)
    print(f"Will perform {len(search_plan.searches)} searches")
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
    print("Performing searches...")
    async def single_search(search_item: WebSearchItem):
        input_text = f"Search term: {search_item.query}\nReason for searching: {search_item.reason}"
        try:
            result = await Runner.run(search_agent, input_text)
            return str(result.final_output)
        except Exception:
            return None
    
    tasks = [asyncio.create_task(single_search(item)) for item in search_plan.searches]
    results = []
    num_completed = 0
    
    for task in asyncio.as_completed(tasks):
        result = await task
        if result is not None:
            results.append(result)
        num_completed += 1
        print(f"Searching... {num_completed}/{len(tasks)} completed")
    print("Finished searching")
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
    print("Writing report...")
    input_text = f"Original query: {query}\nSummarized search results: {search_results}"
    
    result = await Runner.run(writer_agent, input_text)
    report_data = result.final_output_as(ReportData)
    
    print("Finished writing report")
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
        
        yield f"🚀 **Starting Deep Research** for query: *{query}*\n\n"
        yield f"📊 **Trace ID**: {trace_id}\n"
        yield f"🔗 [View trace](https://platform.openai.com/traces/trace?trace_id={trace_id})\n\n"
        
        with trace("Deep Research", trace_id=trace_id):
            try:
                yield "## 🤖 Starting Research Manager Agent\n"
                yield "⚙️ **Agent**: Research Manager is orchestrating the complete research workflow...\n\n"
                yield "🔄 **Process**: The agent will plan searches, execute them, and generate a report\n\n"
                
                # Use the research_manager agent to orchestrate everything
                result = await Runner.run(research_manager, f"Conduct research on: {query}")
                
                yield "✅ **Research Agent Complete!**\n\n"
                yield "---\n\n"
                yield "# 📊 Research Report\n\n"
                yield str(result.final_output)
                
            except Exception as e:
                yield f"❌ **Error occurred**: {str(e)}\n\n"
                yield "Please try again or contact support if the issue persists."

