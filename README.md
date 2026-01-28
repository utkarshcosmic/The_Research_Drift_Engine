The Research Drift Engine is an agentic framework designed to solve "Benchmark Drift" by autonomously cross-referencing research paper lineages (e.g., Llama 2 to Llama 3) against hardware-to-performance metrics.

Key Features
Hierarchical Orchestration: Utilizes a central Deep-Agent coordinator to manage specialized sub-agents for web discovery, academic metadata retrieval, and local PDF parsing.

Custom MCP Integration: Leverages Model Context Protocol (MCP) servers to programmatically extract structured metadata—including VRAM requirements and accuracy benchmarks—from raw PDF text and external APIs.

Drift Analysis Logic: Quantifies "Resource Inflation" by normalizing performance improvements against computational requirements.

Full Observability: Integrated with LangSmith for granular tracing of agent reasoning paths and tool-calling efficiency.

Tech Stack
Orchestration: Deep Agents, LangChain

Models: Gemini 2.5 Flash, Gemini 3 Flash-Preview

Connectivity: MCP (Model Context Protocol), Tavily Search, Semantic Scholar API

Observability: LangSmith

Performance Metrics
~90% Reduction in manual literature review time.

<150s Execution for end-to-end lineage analysis and benchmark synthesis.
