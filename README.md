# Asteroid Research Assistant

An interactive space-science application designed to help users explore, analyze, and learn about Near-Earth Objects (NEOs) and asteroids.

---

## 📌 Project Status: Initial Setup Stage

> **Note:** This project is currently in its initial environment setup stage. Core application features, AI model integrations, and live data queries will be implemented in subsequent phases.

---

## 🚀 Planned Technologies

The project will gradually incorporate the following stack:

- **Python**: Primary programming language for data logic and backend workflows.
- **Streamlit**: Fast, interactive web frontend for displaying asteroid data and AI responses.
- **Large Language Model (LLM)**: An AI model accessed via Hugging Face to answer space-science questions and interpret technical astronomical data.
- **Astronomical Data Source**: Reliable Near-Earth Object (NEO) data (e.g., NASA NeoWs or astronomical databases) for real-world asteroid parameters.

---

## 📂 Project Structure

```text
asteroid-research-assistant/
├── app.py              # Streamlit application entry point (currently Hello World)
├── requirements.txt    # Project Python dependencies (currently streamlit)
├── README.md           # Project documentation and roadmap
└── .gitignore          # Git exclusion rules (.venv, cache, environment files)
```

---

## 💻 How to Run Locally

1. Open your terminal and navigate to the project directory:
   ```bash
   cd asteroid-research-assistant
   ```

2. Activate the virtual environment:
   - **macOS / Linux**:
     ```bash
     source .venv/bin/activate
     ```
   - **Windows (Command Prompt / PowerShell)**:
     ```cmd
     .venv\Scripts\activate
     ```

3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

4. Open the displayed local URL in your web browser (usually `http://localhost:8501`).
