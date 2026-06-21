from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.tool_node import ToolRuntime
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.managed import RemainingSteps
from typing_extensions import TypedDict

# ============================================================
# PARTIE 1 : Définition des outils
# ============================================================

@tool
def read_email(runtime: ToolRuntime) -> str:
    """Read an email from the inbox."""
    return runtime.state["email"]

@tool
def send_email(body: str) -> str:
    """Send an email with the given body. Requires human approval before sending."""
    decision = interrupt({
        "action_requests": [
            {"name": "send_email", "args": {"body": body}}
        ]
    })

    d = decision["decisions"][0]
    if d["type"] == "approve":
        return "Email sent successfully."
    elif d["type"] == "reject":
        return f"Email rejected: {d.get('message', 'No reason given')}"
    elif d["type"] == "edit":
        new_body = d["edited_action"]["args"]["body"]
        return f"Email sent (modified): {new_body}"
    return f"Unknown decision type: {d['type']}"

# ============================================================
# PARTIE 2 : Création de l'agent HITL
# ============================================================

class EmailState(TypedDict):
    messages: Annotated[list, add_messages]
    remaining_steps: RemainingSteps
    email: str

model = ChatOllama(model="llama3.2:3b", temperature=0)
checkpointer = MemorySaver()

agent = create_react_agent(
    model=model,
    tools=[read_email, send_email],
    state_schema=EmailState,
    checkpointer=checkpointer,
)

EMAIL = (
    "Bonjour Sara, je vais être en retard pour notre réunion de demain. "
    "Pouvons-nous la reprogrammer ? Cordialement, Sofia"
)
PROMPT = (
    "Veuillez lire mon e-mail et envoyer une réponse immédiatement. "
    "Envoyez la réponse maintenant dans le même fil de discussion."
)

def invoke_initial(thread_id: str) -> tuple:
    config = {"configurable": {"thread_id": thread_id}}
    response = agent.invoke(
        {"messages": [HumanMessage(content=PROMPT)], "email": EMAIL},
        config,
    )
    return response, config

# ─── Invocation initiale ──────────────────────────────
print("=" * 60)
print("PARTIE 2 : Invocation initiale — interruption avant envoi")
print("=" * 60)
response, config_approve = invoke_initial("thread_approve")
print("\n--- Interrupt info ---")
print(response['__interrupt__'])
print("\n--- Corps du mail proposé par l'agent ---")
print(response['__interrupt__'][0].value['action_requests'][0]['args']['body'])

# ============================================================
# PARTIE 3 : Approuver le résultat
# ============================================================

print("\n" + "=" * 60)
print("PARTIE 3 : Approuver le résultat")
print("=" * 60)
response = agent.invoke(
    Command(resume={"decisions": [{"type": "approve"}]}),
    config_approve,
)
print(response['messages'][-1].content)

# ============================================================
# PARTIE 4 : Refuser le résultat
# ============================================================

print("\n" + "=" * 60)
print("PARTIE 4 : Refuser le résultat")
print("=" * 60)
_, config_reject = invoke_initial("thread_reject")
response = agent.invoke(
    Command(resume={
        "decisions": [{"type": "reject", "message": "J'annule notre rendez-vous."}]
    }),
    config_reject,
)
print(response['messages'][-1].content)

# ============================================================
# PARTIE 5 : Modifier le résultat
# ============================================================

print("\n" + "=" * 60)
print("PARTIE 5 : Modifier le résultat")
print("=" * 60)
_, config_edit = invoke_initial("thread_edit")
response = agent.invoke(
    Command(resume={
        "decisions": [{
            "type": "edit",
            "edited_action": {
                "name": "send_email",
                "args": {"body": "Je suis désolée mais je dois annuler notre rendez-vous je ne serais pas libre. Sara"}
            }
        }]
    }),
    config_edit,
)
print(response['messages'][-1].content)