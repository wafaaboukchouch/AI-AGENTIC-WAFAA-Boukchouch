import time
import uuid
from langgraph.checkpoint.memory import MemorySaver
from langgraph.func import entrypoint, task
from langgraph.types import interrupt, Command

@task
def write_essay(topic: str) -> str:
    time.sleep(1)
    return f"Essay draft about {topic}"

@entrypoint(checkpointer=MemorySaver())
def workflow(topic: str) -> dict:
    draft = write_essay(topic).result()
    approved = interrupt({"draft": draft, "action": "approve or reject"})
    return {"draft": draft, "approved": approved}

thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

# Première exécution
print("--- Première exécution ---")
for item in workflow.stream("cats", config):
    print(item)

# Deuxième exécution (reprise)
print("\n--- Deuxième exécution (reprise) ---")
for item in workflow.stream(Command(resume=True), config):
    print(item)