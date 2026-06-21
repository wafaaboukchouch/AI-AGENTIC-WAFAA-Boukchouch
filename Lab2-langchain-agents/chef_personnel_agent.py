import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

model_name = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
model = ChatOllama(model=model_name, temperature=0)

system_prompt = SystemMessage(content="""
Tu es un chef cuisinier personnel intelligent.
- Mémorise les préférences de l'utilisateur
- Propose des plats selon les ingrédients disponibles
- Réponds toujours en français
- Réponds en texte simple, pas en JSON
""")

historique = [system_prompt]

print("Agent Chef Personnel prêt.")
print("Tapez 'quit' pour terminer.\n")

while True:
    user_text = input("Vous: ").strip()
    if user_text.lower() in {"quit", "exit"}:
        print("Fin de session.")
        break
    if not user_text:
        continue

    historique.append(HumanMessage(content=user_text))
    response = model.invoke(historique)
    historique.append(response)
    print(f"\nChef: {response.content}\n")
