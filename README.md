# Deep Research Using OpenAI SDK

A multi-agent research system that uses OpenAI's agents framework to conduct comprehensive research on any topic. The system employs specialized agents to plan searches, gather information from the web, and synthesize findings into detailed reports.

## Features

- **Multi-Agent Architecture**: Uses specialized agents for different research tasks
  - **Planner Agent**: Plans optimal web searches for a given query
  - **Search Agent**: Performs web searches and summarizes results
  - **Writer Agent**: Synthesizes research into comprehensive reports
- **Web Interface**: Clean, intuitive Gradio-based UI
- **Asynchronous Processing**: Efficient concurrent search execution
- **Detailed Reports**: Generates 1000+ word markdown reports with follow-up questions
- **Trace Monitoring**: Integration with OpenAI's tracing for debugging and monitoring

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │───▶│  Planner Agent  │───▶│  Search Plan    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Final Report    │◀───│  Writer Agent   │◀───│  Search Agent   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Prerequisites

- Python 3.10 or higher
- UV package manager (recommended) or pip
- OpenAI API key

## Installation

### Using UV (Recommended)

1. **Install UV** (if not already installed):
   ```bash
   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and setup the project**:
   ```bash
   git clone <your-repo-url>
   cd "Deep Research Using Open AI SDK"
   uv sync
   ```

### Using pip

```bash
git clone <your-repo-url>
cd "Deep Research Using Open AI SDK"
pip install -r requirements.txt
```

## Configuration

1. **Create environment file**:
   ```bash
   # Create .env file in the project root
   touch .env
   ```

2. **Add your OpenAI API key**:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Optional environment variables**:
   ```env
   # For email functionality (if using email agent)
   SENDGRID_API_KEY=your_sendgrid_api_key_here
   ```

## Running the Application

### Using UV
```bash
uv run python deep_research/deep_research.py
```

### Using Python directly
```bash
python deep_research/deep_research.py
```

The application will start a Gradio web interface that automatically opens in your browser at `http://localhost:7860`.

## Usage

1. **Open the web interface** (launches automatically)
2. **Enter your research query** in the text box
3. **Click "Run"** or press Enter
4. **Monitor progress** as the system:
   - Plans optimal searches
   - Performs web research
   - Synthesizes findings
5. **Review the generated report** with detailed findings and follow-up questions

### Example Queries

- "What are the latest developments in quantum computing?"
- "How does climate change affect marine ecosystems?"
- "What are the economic impacts of artificial intelligence adoption?"
- "Compare different approaches to renewable energy storage"

## Project Structure

```
Deep Research Using Open AI SDK/
├── deep_research/
│   ├── deep_research.py      # Main application entry point
│   ├── research_manager.py   # Orchestrates the research process
│   ├── planner_agent.py     # Plans web searches
│   ├── search_agent.py      # Performs web searches
│   └── writer_agent.py      # Generates final reports
├── pyproject.toml           # Project configuration and dependencies
├── uv.lock                  # Dependency lock file
├── .env                     # Environment variables (create this)
├── .gitignore              # Git ignore patterns
└── README.md               # This file
```

## Development

### Installing development dependencies

```bash
# Using UV
uv sync --dev

# Using pip
pip install -e ".[dev]"
```

### Code formatting and linting

```bash
# Format code
black deep_research/

# Lint code
ruff check deep_research/
```

### Running tests

```bash
pytest
```

## Configuration Options

The system can be customized by modifying the agent configurations:

- **Number of searches**: Modify `HOW_MANY_SEARCHES` in `planner_agent.py`
- **Search context**: Adjust `search_context_size` in `search_agent.py`
- **Report length**: Modify instructions in `writer_agent.py`
- **Model selection**: Change `model` parameter in agent definitions

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your OpenAI API key is set in the `.env` file
2. **Import Errors**: Make sure all dependencies are installed with `uv sync`
3. **Network Issues**: Check your internet connection for web search functionality
4. **Rate Limits**: OpenAI API rate limits may affect performance with large queries

### Debugging

The application provides trace URLs for debugging. When running a query, look for:
```
View trace: https://platform.openai.com/traces/trace?trace_id=<trace_id>
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request



## Support

For support and questions, please contact me: https://www.linkedin.com/in/omaralebda/ 