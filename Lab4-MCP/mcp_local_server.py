from dotenv import load_dotenv
load_dotenv()

from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
from typing import Dict, Any
from requests import get

mcp = FastMCP("mcp_server")
tavily_client = TavilyClient()

@mcp.tool()
def search_web(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    results = tavily_client.search(query)
    return results

@mcp.resource("github://langchain-ai/langchain-mcp-adapters/main/README.md")
def github_file():
    """Resource for accessing langchain-ai/langchain-mcp-adapters/README.md file"""
    url = "https://raw.githubusercontent.com/langchain-ai/langchain-mcp-adapters/main/README.md"
    try:
        resp = get(url)
        return resp.text
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.prompt()
def prompt():
    """Analyze data from a langchain-ai repo file with comprehensive insights"""
    return """
    You are a helpful assistant that answers user questions about LangChain, LangGraph and LangSmith.
    You can use the following tools/resources to answer user questions:
    - search_web: Search the web for information
    - github_file: Access the langchain-ai repo files
    """

if __name__ == "__main__":
    mcp.run(transport="stdio")