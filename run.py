import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.orchestrator.orchestrator import Orchestrator

if __name__ == "__main__":
    import sys
    user_query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Analyze ad performance"
    Orchestrator().run(user_query)
