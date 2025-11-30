import pandas as pd
from src.orchestrator.utils.io_utils import load_prompt
from src.orchestrator.utils.model import call_model

class DataAgent:
    def run(self, data_path):
        df = pd.read_csv(data_path)
        return df.to_dict(orient="records")
