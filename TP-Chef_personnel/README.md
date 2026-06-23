# TP — Agent Chef Cuisinier Personnel Marocain

**Master BDCC — SMA et IAD | Prof. RETAL SARA**  
**Auteur : Wafaa Boukchouch**

---

## 📌 Objectif

Concevoir un agent intelligent jouant le rôle d'un **chef cuisinier personnel marocain halal** capable de :
- Recevoir la liste des ingrédients disponibles
- Mémoriser les préférences et restrictions alimentaires
- Rechercher des recettes via RAG (base locale) et recherche web
- Proposer des plats adaptés aux ingrédients et préférences

---

## 🗂️ Structure du projet
TP-Chef_personnel/

├── chef_agent.py    # Agent chef cuisinier principal

├── recipes.txt      # Base de recettes locales (RAG)

├── images/          # Captures d'écran

├── .env.example     # Exemple de configuration

└── README.md

---

## 🏗️ Architecture de l'agent
Question utilisateur

│

▼

Chef Agent (LLM)

│

├── get_preferences ──────► Récupère les préférences stockées

├── remember_preference ──► Sauvegarde une nouvelle préférence

├── search_recipes_rag ───► Recherche dans la base locale

└── search_web ───────────► Recherche sur internet (Tavily)

---

## ⚙️ Installation

```bash
pip install langchain-ollama langchain-huggingface langgraph langchain-text-splitters python-dotenv
```

---

## 🛠️ Configuration

Copie `.env.example` vers `.env` et remplis :
TAVILY_API_KEY=your_tavily_api_key_here

---

## 🍳 Outils de l'agent

| Outil | Description |
|---|---|
| `search_recipes_rag` | Recherche sémantique dans la base de recettes locale |
| `search_web` | Recherche web via Tavily pour des recettes supplémentaires |
| `remember_preference` | Sauvegarde une préférence dans l'état de l'agent |
| `get_preferences` | Récupère toutes les préférences enregistrées |

---

## 📚 Base de recettes (RAG)

La base locale contient **22 recettes** dont :

- 🇲🇦 **Plats marocains** : Tajine, Couscous, Harira, Pastilla, Mrouzia, Zaalouk, Taktouka, Briouates
- 🌍 **Plats internationaux** : Pasta, Risotto, Curry, Ratatouille, Gratin
- ✅ **Tous halal** : sans alcool, sans porc

---

## 🚀 Exécution

```bash
python chef_agent.py
```

---

## 💬 Exemple de conversation
User  : Je suis marocaine et musulmane, je mange halal uniquement.

Chef  : Bonjour ! Voici 3 recommandations halal :

1. Gratin de courgettes

2. Briouates aux crevettes

3. Mrouzia
User  : Je suis allergique aux arachides.

Chef  : J'ai adapté mes recommandations sans arachides :

1. Gratin de courgettes ✅

2. Briouates au poulet ✅

3. Mrouzia sans amandes ✅
User  : J'ai du poulet, des oignons, de l'ail, du citron confit et des olives.

Chef  : Parfait ! Je vous propose un délicieux Tajine de poulet aux olives

et citron confit !

---

## 🧠 Fonctionnalités clés

| Fonctionnalité | Implémentation |
|---|---|
| **Mémoire** | `MemorySaver` + état `preferences` |
| **RAG** | `HuggingFaceEmbeddings` + `InMemoryVectorStore` |
| **Recherche web** | `TavilySearchResults` |
| **System prompt** | Instructions chef cuisinier marocain halal |
| **Persistance** | `thread_id` pour garder le contexte |

---

## 🛠️ Technologies utilisées

| Package | Rôle |
|---|---|
| `langchain-ollama` | Modèle LLM local (llama3.2:3b) |
| `langchain-huggingface` | Embeddings pour le RAG |
| `langgraph` | Runtime d'agent et mémoire |
| `langchain-text-splitters` | Découpage des recettes en chunks |
| `tavily-python` | Recherche web |

---

## 👩‍💻 Auteur

**Wafaa Boukchouch** — Master BDCC, ENSET Mohammedia