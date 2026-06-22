# Lab 9 — Agent avec LangGraph

**Master BDCC — SMA et IAD | Prof. RETAL SARA**  
**Auteur : Wafaa Boukchouch**

---

## 📌 Objectif

Implémenter un agent LangGraph avancé capable de :
- Utiliser des **tools** arithmétiques
- **Streamer** les résultats en temps réel
- S'arrêter pour **validation humaine** (HITL)
- **Reprendre** après interruption
- **Forker** l'historique pour revenir dans le passé

---

## 🗂️ Structure du projet
Lab9-Agent_avec_LangGraph/

├── tools_setup.py          # Partie 1 : Outils arithmétiques

├── agent_node.py           # Partie 2 : Agent comme nœud LangGraph

├── hitl_workflow.py        # Partie 3 : Workflow HITL

├── tp_advanced_agent.py    # Partie 4 : Agent avancé (HITL + Fork)

├── images/                 # Captures d'écran

└── README.md

---

## ⚙️ Installation

```bash
pip install langchain-ollama langgraph python-dotenv
```

---

## 📄 Partie 1 — LLM avec outils

Trois outils arithmétiques :

| Outil | Description |
|---|---|
| `add(a, b)` | Addition |
| `multiply(a, b)` | Multiplication |
| `divide(a, b)` | Division |

---

## 📄 Partie 2 — Agent comme nœud LangGraph

### Architecture
START → llm_call → should_continue → tool_node → llm_call (boucle)

└─────────────────► END

### Exécution
```bash
python agent_node.py
```

### Résultat obtenu
================================ Human Message =================================

Add 3 and 4.

================================== Ai Message ==================================

Tool Calls: add (args: a=3, b=4)

================================= Tool Message =================================

7

================================== Ai Message ==================================

The sum of 3 and 4 is 7.
--- Stream updates ---

{'llm_call': {...}} → {'tool_node': {'messages': ['1290']}} → {'llm_call': {...}}
--- Stream messages ---

The result of dividing 30 by 43 is approximately 0.6976.

---

## 📄 Partie 3 — Workflow HITL avec @task et @entrypoint

```python
@task
def write_essay(topic: str) -> str:
    return f"Essay draft about {topic}"

@entrypoint(checkpointer=MemorySaver())
def workflow(topic: str) -> dict:
    draft = write_essay(topic).result()
    approved = interrupt({"draft": draft, "action": "approve or reject"})
    return {"draft": draft, "approved": approved}
```

### Exécution
```bash
python hitl_workflow.py
```

### Résultat obtenu
--- Première exécution ---

{'write_essay': 'Essay draft about cats'}

{'interrupt': (Interrupt(value={'draft': '...', 'action': 'approve or reject'}))}
--- Deuxième exécution (reprise) ---

{'workflow': {'draft': 'Essay draft about cats', 'approved': True}}

---

## 📄 Partie 4 — Agent avancé (HITL + Fork)

### Fonctionnalités
- ✅ Interruption avant exécution des tools
- ✅ Approbation → exécution du tool
- ✅ Rejet → annulation
- ✅ Fork → retour dans l'historique

### Exécution
```bash
python tp_advanced_agent.py
```

### Résultat obtenu
Interrupt payload: {'question': 'Approve tool execution?', 'tool_calls': [...]}

Done. Last message: The result of adding 3 and 4 is 7.
Interrupt payload: {'question': 'Approve tool execution?', 'tool_calls': [...]}

Done. Last message: (rejeté)
Forked: {'messages': [...], 'llm_calls': 0}

---

## 🔍 Comparaison des modes de streaming

| Mode | Description |
|---|---|
| `updates` | Affiche chaque modification du state node par node |
| `messages` | Affiche les tokens LLM et métadonnées en temps réel |

---

## 🛠️ Technologies utilisées

| Package | Rôle |
|---|---|
| `langchain-ollama` | Modèle LLM local |
| `langgraph` | Runtime d'agent et graphe |
| `MemorySaver` | Persistance et historique |
| `interrupt()` | Suspension pour validation humaine |
| `Command(resume=...)` | Reprise après décision |

---

## 👩‍💻 Auteur

**Wafaa Boukchouch** — Master BDCC, ENSET Mohammedia