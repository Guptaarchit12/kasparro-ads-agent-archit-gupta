Kasparro Ads Agent is an AI-powered autonomous system designed to analyze Facebook Ads performance, identify issues such as high CPA (Cost Per Acquisition), and generate optimization recommendations using structured multi-agent workflows.

This project uses a modular architecture containing:

Orchestrator Agent – Manages the full analysis pipeline

Core Analysis Agents – CTR analyzer, CVR analyzer, CPC analyzer, Spend analyzer

CPA Analysis Agent – Deep-dive into high CPA issues

Prompt Templates – For consistent structured LLM output

IO & Utility Layer – For safe loading of configs, prompts, and datasets

Project Structure
kasparro-ads-agent/
│
├── run.py
├── README.md
│
├── src/
│   ├── orchestrator/
│   │   ├── orchestrator.py
│   │   └── ...
│   │
│   ├── agents/
│   │   ├── ctr_analyzer.py
│   │   ├── cpc_analyzer.py
│   │   ├── cvr_analyzer.py
│   │   ├── spend_analyzer.py
│   │   ├── cpa_analyzer.py   ← NEW
│   │   └── ...
│   │
│   ├── prompts/
│   │   ├── ctr_analyzer.md
│   │   ├── cpc_analyzer.md
│   │   ├── cvr_analyzer.md
│   │   ├── spend_analyzer.md
│   │   ├── cpa_analyzer.md   ← NEW
│   │   └── ...
│   │
│   ├── utils/
│   │   ├── io_utils.py
│   │   ├── llm_client.py
│   │   └── ...
│   │
│   ├── reports/
│   │   └── generated_reports/
│   │       └── cpa_optimization_report.md ← Auto-generated
│   │
│   └── config/
│       └── config.yaml

 How It Works
1️ Load Config & Prompts

The orchestrator loads configuration files and templated prompts using io_utils.

2️ Initialize Agents

Each analyzer (CTR, CVR, CPC, Spend, CPA) is initialized with its prompt and the shared LLM client.

3️ Multi-Agent Evaluation

Each agent evaluates the ad dataset independently and produces structured findings.

4️ CPA Deep-Dive Analysis

The specialized CPA Agent performs root-cause analysis on:

Targeting issues

Creative fatigue

Low CVR

High CPC

Ad frequency

Audience overlap

Poor placement quality

Funnel drop-offs

5️ Report Generation

The orchestrator compiles insights into a final optimization report saved in:

/src/reports/generated_reports/

Running the Project

Run the main orchestrator:

python run.py


The system will produce:

✔ Full metrics analysis
✔ CPA deep-diagnosis
✔ Optimization recommendations
✔ A clean structured report file

Technologies Used

Python 3.10+

OpenAI GPT-4.1 / GPT-5.1 API

Modular Multi-Agent Architecture

YAML Configs

Prompt-driven AI pipeline

 Features
 Modular multi-agent workflow

Each metric is analyzed by its own expert agent.

Deep CPA optimization engine

Brand-new module to detect exact causes of high CPA.

Config-driven

Prompts, API keys, and thresholds controlled via config.yaml.

Auto-formatted reports

Professional reports generated automatically.

Fully extensible

Easily add new agents, prompts, and workflows.

Example Use Cases

Analyzing high CPA campaigns

Understanding cause of low CTR or CVR

Identifying overspending issues

Suggesting optimization strategies

Assisting performance marketing teams

Automating weekly ads reporting

Contributions

Feel free to submit PRs for additional analyzers, datasets, or integrations.

License

MIT License.
