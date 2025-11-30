from src.orchestrator.utils.io_utils import load_config, load_prompt
from src.orchestrator.utils.model import call_model
from src.orchestrator.utils.logging_utils import save_log

from src.orchestrator.agents.planner import PlannerAgent
from src.orchestrator.agents.data_agent import DataAgent
from src.orchestrator.agents.insight_agent import InsightAgent
from src.orchestrator.agents.evaluator_agent import EvaluatorAgent
from src.orchestrator.agents.creative_agent import CreativeAgent
from src.orchestrator.agents.cpa_analyzer import CPAAnalyzer

class Orchestrator:
    def __init__(self):
        self.settings = load_config("config/settings.yaml")
        self.model_cfg = load_config("config/model_config.yaml")

    def _format_cpa_output(self, cpa_analysis):
        """Format CPA analysis for display"""
        import json
        return json.dumps(cpa_analysis, indent=2)

    def run(self, query):
        log = {"query": query, "steps": []}

        # 1. Planner
        planner = PlannerAgent()
        plan = planner.run(query)
        log["steps"].append({"planner": plan})

        # 2. Data Agent
        data_agent = DataAgent()
        data = data_agent.run(self.settings["data_path"])
        log["steps"].append({"data": data})

        # 3. Insights
        insight_agent = InsightAgent()
        insights = insight_agent.run(data)
        log["steps"].append({"insights": insights})

        # 4. CPA Analysis (if CPA-related query)
        if any(keyword in query.lower() for keyword in ["cpa", "cost per acquisition", "high cpa", "optimization"]):
            cpa_analyzer = CPAAnalyzer()
            cpa_analysis = cpa_analyzer.run(data)
            log["steps"].append({"cpa_analysis": cpa_analysis})
        else:
            cpa_analysis = None

        # 5. Evaluator
        evaluator = EvaluatorAgent()
        evaluation = evaluator.run(insights)
        log["steps"].append({"evaluation": evaluation})

        # 6. Creative
        creative = CreativeAgent()
        creatives = creative.run(insights)
        log["steps"].append({"creatives": creatives})

        save_log(self.settings["logs_path"], log)

        print("\n=== ANALYSIS RESULTS ===")
        
        if cpa_analysis:
            print("\n--- CPA ANALYSIS ---")
            print(self._format_cpa_output(cpa_analysis))
        
        print("\n--- CREATIVE RECOMMENDATIONS ---")
        print(creatives)
