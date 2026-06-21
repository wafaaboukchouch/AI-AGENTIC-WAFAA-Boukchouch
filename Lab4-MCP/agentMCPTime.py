import asyncio
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

async def main():
    client = MultiServerMCPClient(
        {
            "time": {
                "transport": "stdio",
                "command": "python",
                "args": ["-m", "mcp_server_time"],
                "env": {"LOCAL_TIMEZONE": "America/New_York"}
            }
        }
    )

    # get tools
    tools = await client.get_tools()

    # Initialiser le modèle Ollama
    model = ChatOllama(
        model="llama3.2:3b",
    )

    agent = create_react_agent(
        model=model,
        tools=tools,
    )

    question = HumanMessage(content="What time is it in Japan")

    response = await agent.ainvoke(
        {"messages": [question]}
    )

    print(response['messages'][-1].content)

asyncio.run(main())