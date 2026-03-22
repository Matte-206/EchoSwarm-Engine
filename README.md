# 🕸️ EchoSwarm: Enterprise Multi-Agent Social Simulator

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)
![Architecture](https://img.shields.io/badge/architecture-Microservices-orange.svg)
![Status](https://img.shields.io/badge/status-Ready_for_Scale-success.svg)

EchoSwarm is an asynchronous, highly scalable multi-agent simulation engine designed to model complex sociological dynamics, information warfare, and echo chamber formations within digital ecosystems.

Unlike traditional single-threaded LLM wrappers, EchoSwarm is architected as a **Distributed Parametric Engine**, ready to be deployed on Kubernetes clusters for nation-scale data analysis.

## 🚀 The Core Vision

Modern sentiment analysis is reactive. EchoSwarm is predictive. 
By injecting dynamic psychological profiles (Agents) into an asynchronous event loop, companies and research institutes can simulate the impact of news, policies, or product launches on a digital population *before* they happen.

## 🧠 Architectural Highlights

- **Parametric Psychometrics:** Agents are not hardcoded prompts. They are dynamically instantiated via JSON payloads representing traits (Aggressiveness, Rationality, Confirmation Bias).
- **Asynchronous Execution (FastAPI):** The backend is designed to accept massive batches of agent configurations and process them non-blockingly via parallel LLM inference.
- **Sliding Window Memory:** Prevents context degradation (hallucinations) and bypasses strict commercial LLM guardrails by dynamically limiting the memory payload.
- **Live Telemetry & JSON Parsing:** A background algorithmic layer (The Censor) evaluates conversations in real-time, extracting precise vectors (Toxicity, Polarization, Reliability) using robust Regex and JSON parsing, immune to LLM output formatting errors.

## 🏗️ System Architecture

EchoSwarm separates the visualization layer from the computation engine, adhering to strict microservices principles:

1. **`engine/main.py` (The Brain):** A FastAPI backend utilizing `asyncio` and `BackgroundTasks` to queue and execute massive parallel LLM calls. Ready to be integrated with Apache Kafka.
2. **`dashboard/app.py` (The Glass Cockpit):** A Streamlit front-end for localized testing, rapid prototyping, and real-time visualization of the Swarm's telemetry.
3. **Data Layer:** Telemetry is compiled in real-time into Pandas DataFrames, ready for CSV export and integration with distributed Vector Databases (e.g., Pinecone).

## 📊 Telemetry Output

The engine outputs structural data for each simulation tick:
- `Tossicita` (1-10): Risk of hate speech or community guideline violations.
- `Polarizzazione` (1-10): The semantic distance between interacting nodes.
- `Affidabilita` (1-10): The ratio of verifiable facts vs. conspiratorial noise.

## ⚙️ Quickstart (Local Sandbox)

To test the logic locally before deploying the API to a cluster:

```bash
# 1. Install dependencies
pip install fastapi uvicorn streamlit pandas openai

# 2. Run the Visual Dashboard
python -m streamlit run dashboard/app.py

# 3. (Optional) Run the Async Engine
uvicorn engine.main:app --reload