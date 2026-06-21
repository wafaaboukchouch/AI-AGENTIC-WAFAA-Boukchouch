import asyncio
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

async def main():
    client = MultiServerMCPClient(
        {
            "local_server": {
                "transport": "stdio",
                "command": "python",
                "args": ["mcp_local_server.py"],
            }
        }
    )

    # get tools
    tools = await client.get_tools()

    # get resources
    resources = await client.get_resources("local_server")

    # get prompts
    prompt = await client.get_prompt("local_server", "prompt")
    prompt = prompt[0].content

    # Initialiser le modèle Ollama
    model = ChatOllama(
        model="llama3.2:3b",
        temperature=0
    )

    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt=prompt
    )

    config = {"configurable": {"thread_id": "1"}}

    response = await agent.ainvoke(
        {"messages": [HumanMessage(content="Tell me about the langchain-mcp-adapters library")]},
        config=config
    )

    print(response['messages'][-1].content)

asyncio.run(main())