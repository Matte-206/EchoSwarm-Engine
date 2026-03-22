import streamlit as st
import httpx
import time
import pandas as pd

st.set_page_config(page_title="EchoSwarm Dashboard", layout="wide")

st.title("🕸️ EchoSwarm: Enterprise Control Room")
st.markdown("Questa interfaccia comunica con l'API Asincrona del motore core.")

# --- SIDEBAR DI CONFIGURAZIONE ---
with st.sidebar:
    st.header("⚙️ Configurazione Swarm")
    sim_id = st.text_input("ID Simulazione", "SWARM-BETA-001")
    topic = st.text_area("Innesco Sociale", "The government introduces a new social credit system.")
    cycles = st.slider("Cicli di simulazione", 1, 10, 3)
    
    st.divider()
    st.subheader("Profilo Agente 1")
    a1_agg = st.slider("Aggressività", 1, 10, 8, key="a1")
    a1_raz = st.slider("Razionalità", 1, 10, 2, key="a2")
    
    st.subheader("Profilo Agente 2")
    a2_agg = st.slider("Aggressività", 1, 10, 2, key="b1")
    a2_raz = st.slider("Razionalità", 1, 10, 9, key="b2")

# --- MOTORE DI INVIO ---
if st.button("🚀 AVVIA SIMULAZIONE SU MOTORE ASINCRONO", type="primary", use_container_width=True):
    # Prepariamo il pacchetto dati per l'API (Generico e Professionale)
    payload = {
        "simulation_id": sim_id,
        "social_trigger": topic,
        "max_cycles": cycles,
        "agents": [
            {
                "agent_id": "NODE-ALFA",
                "traits": {"aggressiveness": a1_agg, "rationality": a1_raz, "confirmation_bias": 8, "ideology_score": -0.5},
                "base_prompt": "Aggressive skeptic"
            },
            {
                "agent_id": "NODE-BETA",
                "traits": {"aggressiveness": a2_agg, "rationality": a2_raz, "confirmation_bias": 2, "ideology_score": 0.5},
                "base_prompt": "Calm academic"
            }
        ]
    }

    try:
        # Invio all'API FastAPI (main.py)
        with st.spinner("Inviando batch al motore asincrono..."):
            response = httpx.post("http://127.0.0.1:8000/api/v1/simulate", json=payload, timeout=10.0)
            
            if response.status_code == 202:
                st.success(f"✅ Simulazione Accettata! ID: {sim_id}")
                st.info("Il motore sta elaborando i dati in background. Controlla il file JSON nella cartella.")
                
                # Feedback visivo
                progress_bar = st.progress(0)
                for p in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(p + 1)
                st.balloons()
            else:
                st.error(f"Errore Motore: {response.status_code}")
    except Exception as e:
        st.error(f"Impossibile connettersi al motore core: {e}. Assicurati che main.py sia attivo (uvicorn).")

st.divider()
st.subheader("📂 Monitoraggio Output")
st.write("I dati saranno disponibili per l'analisi nel Data Lake locale (JSON).")