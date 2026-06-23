import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.tool_node import ToolRuntime
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.managed import RemainingSteps
from typing_extensions import TypedDict

load_dotenv()

# ============================================================
# RAG — indexation de la base de recettes locale
# ============================================================

RECIPES_FILE = Path(__file__).parent / "recipes.txt"
recipes_text = RECIPES_FILE.read_text(encoding="utf-8")

splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40)
chunks = splitter.create_documents([recipes_text])

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = InMemoryVectorStore.from_documents(chunks, embeddings)

# ============================================================
# État personnalisé
# ============================================================

class ChefState(TypedDict):
    messages: Annotated[list, add_messages]
    remaining_steps: RemainingSteps
    preferences: list[str]

# ============================================================
# Outils
# ============================================================

@tool
def search_recipes_rag(query: str) -> str:
    """Search the local recipe knowledge base for dishes, ingredients, and culinary techniques."""
    docs = vectorstore.similarity_search(query, k=3)
    if not docs:
        return "No matching recipes found in the knowledge base."
    return "\n\n---\n\n".join(d.page_content for d in docs)

@tool
def search_web(query: str) -> str:
    """Search the web for recipes, culinary techniques, and ingredient combinations."""
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        return (
            "Web search not available (TAVILY_API_KEY not configured). "
            "Using the local recipe knowledge base instead."
        )
    try:
        from langchain_community.tools.tavily_search import TavilySearchResults
        tavily = TavilySearchResults(max_results=3)
        results = tavily.invoke({"query": query})
        return "\n\n".join(r.get("content", "") for r in results)
    except Exception as e:
        return f"Web search error: {e}"

@tool
def remember_preference(preference: str, runtime: ToolRuntime) -> Command:
    """Store a user preference (dietary restriction, allergy, favourite cuisine) in long-term memory."""
    try:
        current = list(runtime.state["preferences"])
    except KeyError:
        current = []
    updated = current + [preference]
    return Command(update={
        "preferences": updated,
        "messages": [ToolMessage(
            f"Preference saved: {preference}",
            tool_call_id=runtime.tool_call_id,
        )],
    })

@tool
def get_preferences(runtime: ToolRuntime) -> str:
    """Retrieve all stored user preferences, dietary restrictions, and allergies."""
    try:
        preferences = runtime.state["preferences"]
    except KeyError:
        return "No preferences stored yet."
    if not preferences:
        return "No preferences stored yet."
    return "User preferences: " + " | ".join(preferences)

# ============================================================
# Agent chef cuisinier
# ============================================================

SYSTEM_PROMPT = """Tu es un chef cuisinier personnel marocain et halal.
Tu aides les utilisateurs a decouvrir des plats delicieux avec leurs ingredients disponibles.

Tu as acces a :
- search_recipes_rag: recherche dans la base de recettes locale
- search_web: recherche sur internet pour des recettes supplementaires
- remember_preference: enregistre les preferences, allergies et restrictions alimentaires
- get_preferences: recupere les preferences enregistrees de l'utilisateur

Quand un utilisateur te donne ses ingredients disponibles :
1. Verifie d'abord ses preferences avec get_preferences
2. Recherche dans la base de recettes avec search_recipes_rag
3. Propose 2-3 plats concrets adaptes aux ingredients et preferences
4. Respecte toujours les restrictions alimentaires et allergies
5. Propose des plats halal uniquement

Reponds toujours en francais et sois enthousiaste comme un vrai chef !"""

model = ChatOllama(model="llama3.2:3b", temperature=0)

chef_agent = create_react_agent(
    model=model,
    tools=[search_recipes_rag, search_web, remember_preference, get_preferences],
    state_schema=ChefState,
    checkpointer=MemorySaver(),
    prompt=SYSTEM_PROMPT,
)

# ============================================================
# Demo
# ============================================================

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "chef_demo"}}

    def chat(message: str):
        response = chef_agent.invoke(
            {"messages": [HumanMessage(content=message)], "preferences": []},
            config,
        )
        print(f"\nUser  : {message}")
        print(f"Chef  : {response['messages'][-1].content}")

    print("=" * 60)
    print("DEMO : Agent Chef Cuisinier Personnel Marocain")
    print("=" * 60)

    # Enregistrer les preferences
    chat("Je suis marocaine et musulmane, je mange halal uniquement.")
    chat("Je suis allergique aux arachides.")

    # Suggestions avec les ingredients disponibles
    chat(
        "J'ai dans mon frigo : du poulet, des oignons, de l'ail, "
        "du citron confit, des olives vertes, du cumin et du curcuma. "
        "Qu'est-ce que je peux cuisiner ?"
    )

    # Suivi avec de nouveaux ingredients
    chat("Et si j'ajoute des tomates et des pois chiches, qu'est-ce que je peux faire ?")