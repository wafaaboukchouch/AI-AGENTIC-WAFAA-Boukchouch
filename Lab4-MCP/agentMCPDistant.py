import asyncio
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

async def main():
    client = MultiServerMCPClient(
        {
            "travel_server": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:8000/mcp"
            }
        }
    )

    tools = await client.get_tools()
    print(f"Tools disponibles : {[t.name for t in tools]}")

    model = ChatOllama(model="llama3.2:3b")

    agent = create_react_agent(
        model=model,
        tools=tools,
        checkpointer=MemorySaver(),
        prompt="You are a travel agent. No follow up questions."
    )

    config = {"configurable": {"thread_id": "1"}}

    response = await agent.ainvoke(
        {"messages": [HumanMessage(content="Get me a direct flight from Rabat to Agadir on August 31st")]},
        config=config
    )

    print("\n--- Réponse de l'Agent ---")
    print(response['messages'][-1].content)

asyncio.run(main())