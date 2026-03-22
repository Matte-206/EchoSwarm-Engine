# 🕸️ EchoSwarm Engine v1.0

EchoSwarm is a high-performance, asynchronous multi-agent simulation framework designed to model complex social dynamics and behavioral patterns using Large Language Models (LLMs).

Unlike standard synchronous wrappers, EchoSwarm utilizes a **decoupled microservices architecture** to handle large-scale agent interactions without blocking the main execution thread.

---

## 🚀 Key Architectural Features

* **Asynchronous Core:** Built with FastAPI and `asyncio` to manage parallel LLM inference tasks.
* **Parametric Agent Design:** Agents are instantiated via psychometric vectors (Aggressiveness, Rationality, Bias, Ideology) rather than static prompts.
* **State Persistence:** Automatic telemetry export to structured JSON for post-simulation data analysis and visualization.
* **Scalable Pipeline:** Designed to be integrated with message brokers like RabbitMQ or Kafka for million-agent simulations.

---

## 🏗️ Project Structure

* `main.py`: The high-performance REST API and background worker engine.
* `app.py`: A Streamlit-based control room for real-time simulation management.
* `requirements.txt`: Environment dependencies.

---

## 🚦 Quick Start

### 1. Install Dependencies
```bash
pip install fastapi uvicorn httpx pydantic streamlit pandas

---

### 2. Launch the Engine (Backend)
```bash
uvicorn main:app --reload

### 3. Launch the Dashboard (Frontend)
```bash
streamlit run app.py


📊 Research Goals
This project provides a sandbox for:

Information Warfare: Studying echo chamber formation and narrative spreading.

Social Triggers: Testing the impact of global news on diverse demographic clusters.

Scalability: Analyzing the concurrency limits of LLM-based agents in distributed environments.

Developed for research purposes in Swarm Intelligence and Behavioral Modeling.
