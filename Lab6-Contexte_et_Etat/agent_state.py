from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.tool_node import ToolRuntime
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.managed import RemainingSteps
from typing_extensions import TypedDict

# ============================================================
# PARTIE 5 : Définir un état personnalisé
# ============================================================

class CustomState(TypedDict):
    messages: Annotated[list, add_messages]
    remaining_steps: RemainingSteps
    favourite_colour: str

model = ChatOllama(model="llama3.2:3b", temperature=0)

# ============================================================
# PARTIE 6 : Agent qui modifie un état
# ============================================================

@tool
def update_favourite_colour(favourite_colour: str, runtime: ToolRuntime) -> Command:
    """Update the favourite colour of the user in the state once they've revealed it."""
    return Command(update={
        "favourite_colour": favourite_colour,
        "messages": [ToolMessage(
            "Successfully updated favourite colour",
            tool_call_id=runtime.tool_call_id
        )]
    })

@tool
def read_favourite_colour(runtime: ToolRuntime) -> str:
    """Read the favourite colour of the user from the state."""
    try:
        return runtime.state["favourite_colour"]
    except KeyError:
        return "No favourite colour found in state"

agent = create_react_agent(
    model=model,
    tools=[update_favourite_colour, read_favourite_colour],
    checkpointer=MemorySaver(),
    state_schema=CustomState
)

# --- Tour 1 : révéler la couleur favorite ---
response = agent.invoke(
    {"messages": [HumanMessage(content="My favourite colour is green")]},
    {"configurable": {"thread_id": "1"}}
)
print("--- Partie 6 : Agent qui modifie un état ---")
print(response['messages'][-1].content)

# --- Tour 2 : récupérer la couleur favorite ---
response = agent.invoke(
    {"messages": [HumanMessage(content="What's my favourite colour?")]},
    {"configurable": {"thread_id": "1"}}
)
print("\n--- Partie 6 : Agent qui récupère un état ---")
print(response['messages'][-1].content)