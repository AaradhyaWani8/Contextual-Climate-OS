# Contextual Climate OS
### A Context-Aware Computing Environment Powered by an SLM

## Overview
A Linux-based contextual computing prototype combining weather data, Random Forest classification, context management, role-based intent detection and Qwen 2.5 (1.5B) through Ollama.

## Features
- Heatwave classification using machine learning.
- Context management for weather and user roles.
- Personalised assistance for citizens, farmers, outdoor workers and health workers.
- Local SLM integration using Ollama.
- Interactive Streamlit dashboard.
- Linux experiments: process management, CPU scheduling, producer-consumer synchronisation and LRU page replacement.

## Technologies
Python | Streamlit | Scikit-learn | Pandas | NumPy | Matplotlib | Ollama | Qwen 2.5 (1.5B)

## Run the Project
1. Install Python dependencies: `pip install -r requirements.txt`
2. Install Ollama and run: `ollama pull qwen2.5:1.5b`
3. Start the dashboard: `streamlit run src/dashboard.py`
4. Open `http://localhost:8501`.

## Limitations
This is a Linux user-space contextual application prototype, not a replacement OS kernel. Weather data is synthetic and the classifier is a demonstration, not validated real-world forecasting. The SLM requires a local Ollama service.

## Future Scope
Live weather APIs, IoT integration, persistent context, voice interaction and multilingual advisories.
