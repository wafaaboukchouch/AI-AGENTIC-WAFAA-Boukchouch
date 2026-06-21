# Lab2 - Agent Chef Personnel avec LangChain

## Objectif
Construire un agent conversationnel capable de :
- Mémoriser les préférences alimentaires de l'utilisateur
- Proposer des plats selon les ingrédients disponibles
- Répondre en français

## Technologies utilisées
- Python
- LangChain
- Ollama (llama3.2:3b)
- python-dotenv

## Installation

pip install -r requirements.txt

## Configuration
Copie `.env.example` vers `.env` et remplis les valeurs :

OLLAMA_MODEL=llama3.2:3b
TAVILY_API_KEY=your_tavily_api_key_here
APP_MODE=interactive
OLLAMA_TEMPERATURE=0

## Lancement

python chef_personnel_agent.py

## Exemple d'utilisation
- "Bonjour, je suis Wafaa. Je suis végétarienne et j'adore le piment."
- "J'ai des oeufs, tomates, fromage, oignons et pain. Propose-moi un plat.