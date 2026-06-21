# Lab 6 — L'état et le contexte d'un agent

**Master BDCC — SMA et IAD | Prof. RETAL SARA**  
**Auteur : Wafaa Boukchouch**

---

## 📌 Objectif

Comprendre et mettre en pratique la différence entre **contexte** (données immuables fournies à l'invocation) et **état** (données mutables qui évoluent et persistent pendant la conversation) dans un agent LangChain/LangGraph.

---

## 🗂️ Structure du projet
Lab6-Contexte_et_Etat/

├── agent_context.py   # Parties 1-4 : le contexte (immuable)

├── agent_state.py     # Parties 5-6 : l'état (mutable et persistant)

├── images/            # Captures d'écran des résultats

└── README.md

---

## 💡 Concept : Contexte vs État
CONTEXTE                              ÉTAT

────────────────────                  ────────────────────

Immuable pendant l'invocation         Mutable pendant la conversation

Fourni via invoke(context=...)        Modifié par les tools via Command

Pas persisté entre les appels         Persisté par thread_id (checkpointer)

Ex : couleur favorite initiale        Ex : couleur révélée au fil du chat

---

## ⚙️ Installation

```bash
pip install langchain-ollama langgraph python-dotenv
```

---

## 📄 Partie 1 — Définir le contexte (ColourContext)

```python
@dataclass
class ColourContext:
    favourite_colour: str = "blue"
    least_favourite_colour: str = "yellow"
```

---

## 📄 Partie 2 — Agent sans contexte

L'agent ne peut pas accéder au contexte sans tool dédié.

### Exécution
```bash
python agent_context.py
```

### Résultat obtenu
--- Partie 2 : Agent sans contexte ---

I don't have access to your favourite colour...
--- Partie 3 : Agent avec contexte ---

Your favourite colour is blue.
--- Partie 4 : Changement de contexte ---

Your favourite colour is green.

---

## 📄 Partie 5 — Définir un état personnalisé

```python
class CustomState(TypedDict):
    messages: Annotated[list, add_messages]
    remaining_steps: RemainingSteps
    favourite_colour: str
```

---

## 📄 Partie 6 — Agent qui modifie et récupère l'état

### Exécution
```bash
python agent_state.py
```

### Résultat obtenu
--- Partie 6 : Agent qui modifie un état ---

Successfully updated your favourite colour to green!
--- Partie 6 : Agent qui récupère un état ---

Your favourite colour is indeed green!

---

## 🔍 Comparaison Contexte vs État

| | Contexte | État |
|---|---|---|
| **Mutabilité** | Immuable | Mutable |
| **Origine** | Fourni par l'appelant | Construit pendant la conversation |
| **Persistance** | Aucune | Persisté par `thread_id` |
| **Lecture** | `runtime.context` | `runtime.state[...]` |
| **Écriture** | Impossible | `Command(update={...})` |

---

## 🛠️ Technologies utilisées

| Package | Rôle |
|---|---|
| `langchain-ollama` | Modèle LLM local |
| `langgraph` | Runtime d'agent et gestion de l'état |
| `MemorySaver` | Persistance de l'état par thread |

---

## 👩‍💻 Auteur

**Wafaa Boukchouch** — Master BDCC, ENSET Mohammedia