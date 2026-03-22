import asyncio
import json
import logging
import httpx  # Necessario per chiamate API asincrone
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

# ==========================================
# ENTERPRISE LOGGING CONFIGURATION
# ==========================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("EchoSwarm-Core")

app = FastAPI(
    title="EchoSwarm Distributed Engine",
    description="High-performance asynchronous engine for large-scale multi-agent simulations.",
    version="1.0.0"
)

# ==========================================
# 1. DATA MODELS (Strict Schema Validation)
# ==========================================
class AgentTraits(BaseModel):
    aggressiveness: int = Field(..., ge=1, le=10)
    rationality: int = Field(..., ge=1, le=10)
    confirmation_bias: int = Field(..., ge=1, le=10)
    ideology_score: float = Field(..., ge=-1.0, le=1.0) # -1.0 to 1.0 scale

class AgentNode(BaseModel):
    agent_id: str
    traits: AgentTraits
    base_prompt: str

class SimulationBatch(BaseModel):
    simulation_id: str
    social_trigger: str
    agents: List[AgentNode]
    max_cycles: int = Field(..., ge=1, le=100)
    llm_endpoint: Optional[str] = "http://localhost:11434/api/generate" # Default to local Ollama

# ==========================================
# 2. ASYNC INFERENCE ENGINE
# ==========================================
async def call_llm_async(endpoint: str, system_prompt: str, user_input: str) -> dict:
    """
    Gestisce l'inferenza asincrona verso il cluster LLM (Ollama/Custom).
    """
    payload = {
        "model": "llama3.2",
        "prompt": f"System: {system_prompt}\nUser: {user_input}",
        "stream": False,
        "format": "json" # Forza Ollama a rispondere in JSON
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(endpoint, json=payload)
            if response.status_code == 200:
                # Estraiamo la risposta testuale e la carichiamo come JSON
                raw_content = response.json().get("response", "{}")
                return json.loads(raw_content)
            return {"error": "Inference failed", "status": response.status_code}
    except Exception as e:
        logger.error(f"Inference Error: {str(e)}")
        return {"error": str(e)}

# ==========================================
# 3. DISTRIBUTED SIMULATION WORKER
# ==========================================
async def run_distributed_simulation(batch: SimulationBatch):
    logger.info(f"Starting simulation {batch.simulation_id} with {len(batch.agents)} nodes.")
    
    final_results = []
    current_context = f"Initial Trigger: {batch.social_trigger}"

    for cycle in range(batch.max_cycles):
        logger.info(f"Processing Cycle {cycle + 1}/{batch.max_cycles} | ID: {batch.simulation_id}")
        
        tasks = []
        for agent in batch.agents:
            # Costruiamo il prompt dinamico basato sui tratti psicometrici
            system_p = (
                f"Role: {agent.base_prompt}. Traits: Aggressiveness={agent.traits.aggressiveness}, "
                f"Rationality={agent.traits.rationality}. Respond in JSON: {{'text': '...', 'toxicity': 1-10}}"
            )
            tasks.append(call_llm_async(batch.llm_endpoint, system_p, current_context))
        
        # Esecuzione parallela massiva (I/O Bound)
        cycle_responses = await asyncio.gather(*tasks)
        
        # Aggiornamento contesto per il ciclo successivo (Sliding Window)
        cycle_summary = " ".join([r.get("text", "") for r in cycle_responses if "text" in r])
        current_context = cycle_summary[-1000:] # Mantieni solo gli ultimi 1000 caratteri

        final_results.append({
            "cycle": cycle + 1,
            "agent_data": cycle_responses
        })

    # Data Persistence (Simulazione di un Data Lake)
    output_file = f"telemetry_{batch.simulation_id}.json"
    with open(output_file, "w") as f:
        json.dump(final_results, f, indent=4)
    logger.info(f"Simulation {batch.simulation_id} storage completed: {output_file}")

# ==========================================
# 4. API ENDPOINTS
# ==========================================
@app.post("/api/v1/simulate", status_code=202)
async def start_simulation(batch: SimulationBatch, background_tasks: BackgroundTasks):
    """
    Entry point per il caricamento di batch massivi di agenti.
    Ritorna 202 Accepted per indicare l'avvio del processo asincrono.
    """
    if not batch.agents:
        raise HTTPException(status_code=400, detail="Agent list cannot be empty.")
    
    background_tasks.add_task(run_distributed_simulation, batch)
    
    return {
        "status": "accepted",
        "simulation_id": batch.simulation_id,
        "nodes_queued": len(batch.agents),
        "info": "Execution pushed to background worker."
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "engine": "EchoSwarm-Core"}