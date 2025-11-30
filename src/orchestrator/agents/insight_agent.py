from src.orchestrator.utils.model import call_model
from src.orchestrator.utils.io_utils import load_prompt

class InsightAgent:
    def run(self, data):
        prompt = load_prompt("config/prompts/insight_agent.md")
        return call_model(prompt.format(data=data))
