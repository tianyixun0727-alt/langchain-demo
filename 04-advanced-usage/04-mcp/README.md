# 4.4 Model Context Protocol (MCP)

MCP is an open standard that connects AI models with external tools and data sources. It defines how models discover and call external capabilities, enabling a plug-and-play ecosystem of tools, services, and knowledge bases.

| File | Description |
|------|-------------|
| `01_overview.py` | MCP concepts, benefits, and how it works |
| `02_client_demo.py` | Connect to an MCP server and use MCP tools in an agent |

## Key Concepts

- **Dynamic tool discovery** — Models discover available tools at runtime through an MCP server
- **Standardized protocol** — Uniform interface for tools, resources, and prompts across providers
- **Secure execution** — Sandboxed tool execution with configurable permissions
- **LangChain integration** — LangChain agents can use MCP tools like any other tool
