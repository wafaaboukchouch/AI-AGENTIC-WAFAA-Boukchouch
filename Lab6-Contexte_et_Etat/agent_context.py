from dataclasses import dataclass
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.tool_node import ToolRuntime

# ============================================================
# PARTIE 1 : Définir une classe de contexte ColourContext
# ============================================================

@dataclass
class ColourContext:
    favourite_colour: str = "blue"
    least_favourite_colour: str = "yellow"

model = ChatOllama(model="llama3.2:3b", temperature=0)

# ============================================================
# PARTIE 3 : Tools qui lisent le contexte
# ============================================================

@tool
def get_favourite_colour(runtime: ToolRuntime) -> str:
    """Get the favourite colour of the user"""
    return runtime.context.favourite_colour

@tool
def get_least_favourite_colour(runtime: ToolRuntime) -> str:
    """Get the least favourite colour of the user"""
    return runtime.context.least_favourite_colour

# ============================================================
# PARTIE 2 : Agent sans accès au contexte
# ============================================================

agent_no_context = create_react_agent(
    model=model,
    tools=[get_favourite_colour, get_least_favourite_colour],
    context_schema=ColourContext
)

response = agent_no_context.invoke(
    {"messages": [HumanMessage(content="What is my favourite colour?")]},
    context=ColourContext()
)
print("--- Partie 2 : Agent sans contexte ---")
print(response['messages'][-1].content)

# ============================================================
# PARTIE 3 : Agent avec contexte
# ============================================================

agent_with_context = create_react_agent(
    model=model,
    tools=[get_favourite_colour, get_least_favourite_colour],
    context_schema=ColourContext
)

response = agent_with_context.invoke(
    {"messages": [HumanMessage(content="What is my favourite colour?")]},
    context=ColourContext()
)
print("\n--- Partie 3 : Agent avec contexte ---")
print(response['messages'][-1].content)

# ============================================================
# PARTIE 4 : Changement de contexte
# ============================================================

response = agent_with_context.invoke(
    {"messages": [HumanMessage(content="What is my favourite colour?")]},
    context=ColourContext(favourite_colour="green")
)
print("\n--- Partie 4 : Changement de contexte ---")
print(response['messages'][-1].content)