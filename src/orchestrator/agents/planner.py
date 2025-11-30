from src.orchestrator.utils.model import call_model
from src.orchestrator.utils.io_utils import load_prompt

class PlannerAgent:
    def run(self, query):
        prompt = load_prompt("config/prompts/planner.md")
        return call_model(prompt.format(query=query))
