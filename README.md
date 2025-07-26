# Deep Research Using OpenAI SDK

An advanced multi-agent research system using OpenAI's agents framework to automate comprehensive topic research, leveraging AI to plan, execute, and synthesize findings.

## Features

* Intelligent search query planning
* Concurrent web searches for efficiency
* Synthesizing detailed research reports
* User-friendly Gradio UI with real-time progress
* Transparent AI agent activity tracing

## Project Structure Overview

```plaintext
Deep Research Using OpenAI SDK/
├── deep_research/
│   ├── deep_research.py        # Web Interface (Gradio)
│   ├── research_manager.py     # Coordinates agent workflows
│   ├── planner_agent.py        # Generates search queries
│   ├── search_agent.py         # Executes web searches
│   └── writer_agent.py         # Generates research reports
├── .env                        # API key configuration
├── requirements.txt            # Project dependencies
├── pyproject.toml              # Project configuration
└── README.md                   # Documentation
```

## How the System Works

The system consists of three specialized AI agents coordinated by a central Research Manager:

### Workflow

1. **Planner Agent**: Breaks user queries into targeted search terms.
2. **Search Agent**: Performs multiple concurrent searches and summarizes results.
3. **Writer Agent**: Compiles search results into a structured markdown report.

### Tools Used by the Research Manager

* **plan\_research\_searches**: Generates structured search queries from user input.
* **perform\_multiple\_searches**: Concurrently executes planned searches.
* **write\_research\_report**: Creates a cohesive markdown research report from search summaries.

## Quick Start

### Setup Requirements

* Python 3.10+
* OpenAI API Key

### Installation

```bash
# Install UV package manager
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup project
git clone <repository-url>
cd "Deep Research Using Open AI SDK"
uv sync

# Configure environment
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# Run application
uv run python deep_research/deep_research.py
```

## Accessing the Interface

Open your browser at `http://127.0.0.1:7860` to start using the tool.

## Configuration Options

| Setting      | File Location      | Default       | Description        |
| ------------ | ------------------ | ------------- | ------------------ |
| Search Count | `planner_agent.py` | 5             | Searches per query |
| Model        | All agents         | `gpt-4o-mini` | AI model used      |
| Port         | `deep_research.py` | 7860          | Web interface port |

## Dependencies

* `openai-agents`, `gradio`, `pydantic`, `aiohttp`, `python-dotenv`

## Contributing

* Fork repository
* Create branch, commit changes, and push
* Submit pull request

## Contact

[Omar Alebda - LinkedIn](https://www.linkedin.com/in/omaralebda/)
