# Lab 4 — Model Context Protocol (MCP)

**Master BDCC — SMA et IAD | Prof. RETAL SARA**  
**Auteur : Wafaa Boukchouch**

---

## 📌 Objectif

Intégrer le **Model Context Protocol (MCP)** avec LangChain pour connecter des agents LLM à des serveurs MCP locaux et distants via différents transports (stdio, HTTP streaming). Ce lab explore trois scénarios complémentaires d'utilisation du protocole MCP.

---

## 🗂️ Structure du projet
Lab4-MCP/

├── mcp_local_server.py      # Serveur MCP local (stdio) — tools, resources, prompts

├── mcp_http_server.py       # Serveur MCP HTTP (streamable-http)

├── agentMCP.py              # Partie 1 : Agent avec serveur MCP local

├── agentMCPTime.py          # Partie 2 : Agent avec serveur MCP de temps

├── agentMCPDistant.py       # Partie 3 : Agent avec serveur MCP distant HTTP

├── images/                  # Captures d'écran des résultats

├── .env                     # Variables d'environnement (non versionné)

├── .env.example             # Exemple de configuration

└── README.md

---

## ⚙️ Prérequis

- Python >= 3.10
- [Ollama](https://ollama.com/) avec le modèle `llama3.2:3b`
- Clé API Tavily (optionnelle pour la recherche web)

---

## 🚀 Installation

```bash
pip install langchain-mcp-adapters mcp fastmcp mcp-server-time langchain-ollama tavily-python langgraph python-dotenv requests
```

---

## 🏗️ Architecture MCP
Agent LLM (LangChain)

│

└── MultiServerMCPClient

│

├── stdio transport ──────► mcp_local_server.py

├── stdio transport ──────► mcp-server-time

└── streamable-http ──────► http://127.0.0.1:8000/mcp

---

## 📄 Partie 1 — Agent MCP Local (stdio)

Le serveur `mcp_local_server.py` expose :
- **Tool** : `search_web` — recherche web via Tavily
- **Resource** : README du dépôt `langchain-mcp-adapters`
- **Prompt** : système de l'assistant LangChain

### Exécution
```bash
python agentMCP.py
```

### Résultat obtenu
LangChain is an open-source framework for building custom AI models

and applications. The langchain-mcp-adapters library is part of the

LangChain ecosystem...

---

## ⏰ Partie 2 — Agent MCP Time Server

Utilise le package `mcp-server-time` pour exposer l'heure en temps réel par timezone.

### Exécution
```bash
python agentMCPTime.py
```

### Résultat obtenu
The current time in Japan is 2:09 AM JST (Japan Standard Time).

---

## 🌐 Partie 3 — Agent MCP Distant (HTTP Streaming)

Connexion à un serveur MCP via le transport `streamable-http`. Le serveur expose des outils de recherche de vols.

### Exécution

**Terminal 1 — Lancer le serveur :**
```bash
python mcp_http_server.py
```

**Terminal 2 — Lancer l'agent :**
```bash
python agentMCPDistant.py
```

### Résultat obtenu
Tools disponibles : ['search_flights', 'get_flight_price']

Flight AT601: Departing at 08:00, arriving at 09:15 with Atlas Blue
Flight AT603: Departing at 14:30, arriving at 15:45 with Atlas Blue
Flight AT605: Departing at 19:00, arriving at 20:15 with Atlas Blue


---

## 🔍 Comparaison des transports MCP

| | Partie 1 — stdio | Partie 2 — stdio | Partie 3 — HTTP |
|---|---|---|---|
| **Transport** | stdio | stdio | streamable-http |
| **Serveur** | Script Python local | mcp-server-time | Uvicorn HTTP |
| **Tools** | search_web | get_current_time | search_flights |
| **Usage** | Recherche web + RAG | Heure par timezone | Agent de voyage |

---

## 🛠️ Technologies utilisées

| Package | Rôle |
|---|---|
| `langchain-mcp-adapters` | Client MCP pour LangChain |
| `mcp` | Implémentation du protocole MCP |
| `fastmcp` | Framework serveur MCP |
| `mcp-server-time` | Serveur MCP de temps |
| `langchain-ollama` | Modèle LLM local |
| `langgraph` | Runtime d'agent |
| `uvicorn` | Serveur HTTP ASGI |

---

## 👩‍💻 Auteur

**Wafaa Boukchouch** — Master BDCC, ENSET Mohammedia