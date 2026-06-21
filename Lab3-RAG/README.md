markdown# Lab3 - Retrieval-Augmented Generation (RAG)

## 📌 Objectif

Implémenter le pattern **RAG (Génération Augmentée par Récupération)** avec LangChain pour permettre à un agent LLM de répondre à des questions en se basant sur des sources de données externes.

---

## 🗂️ Structure du projet
Lab3-RAG/

├── part1_rag_pdf.py                  # Partie 1 : Agent RAG sur PDF

├── part2_sql_agent.py                # Partie 2 : Agent SQL sur SQLite

├── acmecorp-employee-handbook.pdf    # Document source

├── Chinook.db                        # Base de données SQLite

├── images/                           # Captures d'écran

└── README.md

---

## 🧠 Concept RAG
Sans RAG : Question → LLM → Réponse potentiellement incorrecte
Avec RAG : Question → Retrieval (documents pertinents)

│

▼

LLM + Contexte récupéré → Réponse précise

---

## ⚙️ Installation

```bash
pip install langchain langchain-community langchain-ollama langgraph sentence-transformers pypdf sqlalchemy
```

---

## 📄 Partie 1 — Agent RAG sur fichier PDF

### Pipeline
PDF → Chargement → Segmentation → Embeddings → VectorStore → Recherche → Agent

### Étapes

| Étape | Outil | Description |
|---|---|---|
| Chargement | `PyPDFLoader` | Extrait le texte du PDF |
| Segmentation | `RecursiveCharacterTextSplitter` | Découpe en chunks (1000 chars) |
| Embeddings | `HuggingFaceEmbeddings` | Vectorise chaque chunk |
| Vector Store | `InMemoryVectorStore` | Stocke les vecteurs en mémoire |
| Recherche | `similarity_search()` | Retrouve les chunks pertinents |
| Agent | `create_react_agent` | Répond aux questions via RAG |

### Exécution

```bash
python part1_rag_pdf.py
```

### Résultat obtenu
Pages chargées : 1

Nombre de chunks : 3

Documents indexés : 3
--- Résultat de la recherche sémantique ---

Paid Time Off (PTO) Policy...
--- Réponse de l'Agent RAG ---

According to the handbook, in an employee's first year,

they accrue 10 days of PTO per year (0.833 days per month).

---

## 🗄️ Partie 2 — Agent SQL sur base SQLite

### Pipeline
Question NL → Agent LLM → sql_query tool → SQLite → Résultat → Réponse NL

### Exécution

```bash
python part2_sql_agent.py
```

### Résultat obtenu
--- Réponse de l'Agent SQL ---

The first five artists in the database are:

AC/DC
Accept
Aerosmith
Alanis Morissette
Alice In Chains


---

## 🔍 Comparaison des deux approches

| | Partie 1 — RAG PDF | Partie 2 — SQL Agent |
|---|---|---|
| **Source** | Fichier PDF | Base SQLite |
| **Recherche** | Similarité sémantique | Requêtes SQL exactes |
| **LLM rôle** | Synthèse du contexte | Génération de requêtes SQL |
| **Meilleur pour** | Questions ouvertes | Données structurées |

---

## 🛠️ Technologies utilisées

- Python 3.10+
- LangChain
- LangGraph
- Ollama (llama3.2:3b)
- HuggingFace Sentence Transformers
- SQLite

---

## 👩‍💻 Auteur

**Wafaa Boukchouch** — Master BDCC, ENSET