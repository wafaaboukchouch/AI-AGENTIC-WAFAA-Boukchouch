# Lab 5 — Multi-Agents & LangGraph Studio

**Master BDCC — SMA et IAD | Prof. RETAL SARA**  
**Auteur : Wafaa Boukchouch**

---

## 📌 Objectif

Implémenter un système **Multi-Agents** avec LangChain et visualiser le graphe d'exécution avec **LangGraph Studio**.

---

## 🗂️ Structure du projet
Lab5-LangGraph_Studio/

├── multi_agents.py      # Système multi-agents (agent principal + sous-agents)

├── agent_simple.py      # Agent RAG simple pour LangGraph Studio

├── langgraph.json       # Configuration LangGraph Studio

├── images/              # Captures d'écran

├── .env.example         # Exemple de configuration

└── README.md

---

## ⚙️ Installation

```bash
pip install langchain-ollama langgraph langgraph-cli python-dotenv
pip install -U "langgraph-cli[inmem]"
```

---

## 🤖 Partie 1 — Système Multi-Agents

### Architecture
Question utilisateur

│

▼

Agent Principal

│

├── call_subagent_1 ──► Sous-Agent 1 (square_root)

└── call_subagent_2 ──► Sous-Agent 2 (square)

### Outils définis

| Outil | Description |
|---|---|
| `square_root` | Calcule la racine carrée |
| `square` | Calcule le carré |
| `call_subagent_1` | Appelle le sous-agent 1 |
| `call_subagent_2` | Appelle le sous-agent 2 |

### Exécution

```bash
python multi_agents.py
```

### Résultat obtenu
The square root of 456 is approximately 21.3542.

---

## 🎨 Partie 2 — LangGraph Studio

### Configuration

Créer un fichier `langgraph.json` :

```json
{
  "graphs": {
    "agent_simple": "./agent_simple.py:agent"
  },
  "env": "./.env",
  "source": {
    "kind": "uv",
    "root": "."
  }
}
```

### Lancement

```bash
C:\Users\HP\AppData\Local\Python\pythoncore-3.14-64\Scripts\langgraph.exe dev
```

### URL Studio
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

### Fonctionnalités de LangGraph Studio

- ✅ Visualisation du graphe (nodes, edges)
- ✅ Exécution étape par étape
- ✅ Envoi de messages (HumanMessage)
- ✅ Inspection des inputs/outputs
- ✅ Débogage des outils

---

## 🛠️ Technologies utilisées

| Package | Rôle |
|---|---|
| `langchain-ollama` | Modèle LLM local |
| `langgraph` | Runtime d'agent |
| `langgraph-cli` | Interface Studio |
| `langsmith` | Monitoring et traçage |

---

## 👩‍💻 Auteur

**Wafaa Boukchouch** — Master BDCC, ENSET Mohammedia