# Lab 7 — Un agent HITL (Human-In-The-Loop)

**Master BDCC — SMA et IAD | Prof. RETAL SARA**  
**Auteur : Wafaa Boukchouch**

---

## 📌 Objectif

Implémenter un agent IA dont l'exécution peut être **interrompue** pour demander une validation humaine avant de continuer — en utilisant `interrupt()` de LangGraph.

---

## 🗂️ Structure du projet
Lab7-Human_In_The_Loop/

├── agent_hitl.py    # Les 5 parties HITL

├── images/          # Captures d'écran des résultats

└── README.md

---

## 💡 Concept HITL
Agent exécute          Humain décide            Agent continue

─────────────          ─────────────            ──────────────

read_email()  ───────► ◄─ interrupt() ─►  ───► approve / reject / edit

send_email()  bloqué   décision requise         résume avec Command(...)

---

## ⚙️ Installation

```bash
pip install langchain-ollama langgraph python-dotenv
```

---

## 📄 Partie 1 — Définition des outils

| Outil | Description |
|---|---|
| `read_email` | Lit un email depuis l'état de l'agent |
| `send_email` | Envoie un email après validation humaine |

---

## 📄 Partie 2 — Invocation initiale

L'agent lit l'email, rédige une réponse puis **s'interrompt** avant d'envoyer.

### Exécution
```bash
python agent_hitl.py
```

### Résultat obtenu
PARTIE 2 : Invocation initiale — interruption avant envoi

--- Interrupt info ---

[Interrupt(value={'action_requests': [{'name': 'send_email', 'args': {'body': '...'}}]})]

--- Corps du mail proposé par l'agent ---

Réponse à votre e-mail : ...

---

## 📄 Partie 3 — Approuver le résultat

```python
Command(resume={"decisions": [{"type": "approve"}]})
```

### Résultat obtenu
Votre e-mail a été envoyé avec succès !

---

## 📄 Partie 4 — Refuser le résultat

```python
Command(resume={"decisions": [{"type": "reject", "message": "J'annule notre rendez-vous."}]})
```

### Résultat obtenu
Désolé(e) Sofia, malheureusement nous ne pouvons pas annuler notre rendez-vous...

---

## 📄 Partie 5 — Modifier le résultat

```python
Command(resume={"decisions": [{"type": "edit", "edited_action": {"name": "send_email", "args": {"body": "..."}}}]})
```

### Résultat obtenu
Email sent (modified): Je suis désolée mais je dois annuler notre rendez-vous...

---

## 🔍 Les 3 décisions HITL

| Type | Comportement |
|---|---|
| `approve` | Envoie le mail tel quel |
| `reject` | Annule l'envoi et retourne la raison au LLM |
| `edit` | Remplace les arguments et envoie le mail modifié |

---

## 🛠️ Technologies utilisées

| Package | Rôle |
|---|---|
| `langchain-ollama` | Modèle LLM local |
| `langgraph` | Runtime d'agent |
| `interrupt()` | Suspension de l'exécution pour validation humaine |
| `Command(resume=...)` | Reprise après décision humaine |
| `MemorySaver` | Persistance par thread |

---

## 👩‍💻 Auteur

**Wafaa Boukchouch** — Master BDCC, ENSET Mohammedia