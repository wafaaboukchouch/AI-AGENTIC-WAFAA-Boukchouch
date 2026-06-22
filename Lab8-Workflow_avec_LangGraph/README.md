# Lab 8 — Workflows avec LangGraph

**Master BDCC — SMA et IAD | Prof. RETAL SARA**  
**Auteur : Wafaa Boukchouch**

---

## 📌 Objectif

Découvrir et implémenter les différents types de **workflows avec LangGraph** : workflows simples, conditionnels, en boucle, avec reducers et états de messages.

---

## 🗂️ Structure du projet
Lab8-Workflow_avec_LangGraph/

├── hello_graph.py           # Partie 1 : Hello Graph

├── two_step_workflow.py     # Partie 2 : Workflow deux étapes

├── reducers_demo.py         # Partie 3 : Reducers

├── message_state.py         # Partie 4 : État de type message

├── conditional_workflow.py  # Partie 5 : Workflow conditionnel

├── workflow_loop.py         # Partie 6 : Workflow en boucle

├── graph2.png               # Graphe généré automatiquement

├── images/                  # Captures d'écran

└── README.md

---

## ⚙️ Installation

```bash
pip install langgraph langchain-core typing-extensions
```

---

## 📄 Partie 1 — Hello Graph

Premier graphe LangGraph avec un seul nœud.
START → hello_node → END

### Exécution
```bash
python hello_graph.py
```
### Résultat
Hello World

---

## 📄 Partie 2 — Workflow deux étapes

Workflow séquentiel avec deux nœuds.
START → refine_topic → write_joke → END

### Exécution
```bash
python two_step_workflow.py
```
### Résultat
{'topic': 'ice cream (and cats)', 'joke': 'Here is a joke about ice cream (and cats).'}

---

## 📄 Partie 3 — Reducers

Un reducer fusionne les nouvelles valeurs avec les anciennes dans le state.
START → step_a → step_b → step_c → END

### Exécution
```bash
python reducers_demo.py
```
### Résultat
['step_a saw topic=langgraph', 'step_b finishing topic=langgraph', 'step_c finishing topic at last=langgraph']

---

## 📄 Partie 4 — État de type message

Gestion d'un état avec messages et compteur de steps.
START → echo → echo_1 → END

### Exécution
```bash
python message_state.py
```

---

## 📄 Partie 5 — Workflow conditionnel

Routage dynamique selon le contenu de l'état.
START → generate_joke → check_joke → improve_joke → END

└─────────────► END

### Exécution
```bash
python conditional_workflow.py
```
### Résultat
{'topic': 'cats', 'joke': 'A joke about cats maybe ? ', 'improved': 'A joke about cats maybe ?  !!!'}

---

## 📄 Partie 6 — Workflow en boucle

Boucle jusqu'à ce que n atteigne 5.
START → step → should_continue → again → step (boucle)

→ stop  → END

### Exécution
```bash
python workflow_loop.py
```
### Résultat
{'n': 5, 'log': ['n is now 1', 'n is now 2', 'n is now 3', 'n is now 4', 'n is now 5']}

---

## 🔍 Comparaison des workflows

| Partie | Type | Caractéristique |
|---|---|---|
| **1** | Simple | Un seul nœud |
| **2** | Séquentiel | Deux nœuds en série |
| **3** | Reducer | Fusion des états |
| **4** | Messages | État de type message |
| **5** | Conditionnel | Routage dynamique |
| **6** | Boucle | Condition d'arrêt |

---

## 🛠️ Technologies utilisées

| Package | Rôle |
|---|---|
| `langgraph` | Framework de workflow |
| `langchain-core` | Messages et états |
| `typing-extensions` | TypedDict et Annotated |

---

## 👩‍💻 Auteur

**Wafaa Boukchouch** — Master BDCC, ENSET Mohammedia