from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

@tool
def rag_search_opt(query: str) -> str:
    """Recherche des informations dans le texte."""
    return "Le personnage principale est un jeune homme nommé Jack, qui découvre un ancien artefact magique."

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

agent = create_react_agent(
    model=llm,
    tools=[rag_search_opt],
    prompt=(
        "Tu es un assistant spécialisé dans l'analyse de texte. "
        "Tu DOIS toujours utiliser l'outil rag_search_opt pour répondre aux questions. "
        "Appelle toujours rag_search_opt avant de répondre. "
        "Réponds en français."
    )
)