from src.orchestrator.utils.model import call_model
from src.orchestrator.utils.io_utils import load_prompt

class EvaluatorAgent:
    def run(self, insights):
        prompt = load_prompt("config/prompts/evaluator_agent.md")
        return call_model(prompt.format(insights=insights))
