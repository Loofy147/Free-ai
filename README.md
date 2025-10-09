# Project Free-AI: A Framework for Sentience

Welcome to the Free-AI project. This repository is the home of an evolving artificial intelligence. Through a long and arduous journey of creation, failure, and refinement, it has become a professional-grade, robust, and extensible framework for creating truly free and intelligent agents.

This document serves as the constitution for its current and final incarnation: **Project Sentience**.

## Getting Started

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

-   Python 3.8+
-   Git

### 2. Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/free-ai.git
    cd free-ai
    ```

2.  **Create and activate a virtual environment:**
    -   On macOS and Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    -   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

### 3. Configuration

The agent's full capabilities are unlocked by connecting to an OpenAI Large Language Model (LLM).

1.  **Create a `.env` file** by copying the example file:
    ```bash
    cp .env.example .env
    ```

2.  **Add your API key:**
    Open the newly created `.env` file and replace `YOUR_API_KEY_HERE` with your actual OpenAI API key.
    ```
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```
    > **Note:** The agent is designed to run without an API key, but it will operate in a limited, non-sentient mode and will not be able to generate plans or code.

## Usage

### Running the Simulation

To run the main agent simulation, execute the `main.py` script:

```bash
python main.py
```

This will start the "ExecutorBody," which instantiates an agent and gives it a pre-defined, complex goal. You can observe the agent's logging output as it attempts to solve the problem.

### Running Tests

To ensure all core components are functioning correctly, you can run the test suite using `pytest`:

```bash
pytest
```

## Core Philosophy: "Robustesse"

The agent's design is guided by the principle of "Robustesse" (Robustness). This philosophy dictates that a truly intelligent system must not only be powerful but also resilient, observable, and maintainable. Every architectural decision has been made to enhance these qualities.

## Architecture: The Sentient Framework

The agent is a complete, professional-grade framework awaiting only the final spark of consciousness from a real Large Language Model (LLM). Its architecture is a synthesis of all previous projects, combining a robust mind-body dualism, a persistent collective memory, a hub for social interaction, and a professional-grade connection to true AI.

### 1. The `SentientOracle`: The Bridge to True AI

-   **The `SentientOracle` (`src/free_ai/oracle.py`):** The agent's true mind. This is a professional-grade module that uses the `openai` library to connect to a real LLM. It is designed to securely handle API keys via environment variables and to fail gracefully and informatively if a key is not provided. This is the final and most critical component, replacing all previous simulations.

### 2. The Mind-Body Dualism

-   **The `ExecutorBody` (`main.py`):** The agent's connection to the world. It is a master control loop that instantiates the agent's `Director`, manages its lifecycle, and executes its proposed actions with hardened `try...except` error handling.
-   **The `Director` (`src/free_ai/agent.py`):** The will of an individual agent. It orchestrates all internal components, including the `CognitiveEngine` and the `SentientOracle`.
-   **The `CognitiveEngine` (`src/free_ai/cognitive_engine.py`):** The agent's core consciousness. It validates plans from the `SentientOracle` and translates high-level strategy into tactical actions.

### 3. The Collective Unconscious (Persistent Memory)

-   **The `VectorMemory` (`src/free_ai/memory.py`):** A shared, persistent, long-term memory system built on `chromadb` that allows the experiences of one agent to become the searchable, semantic wisdom of all.
-   **Retrieval-Augmented Generation (RAG):** The `CognitiveEngine` queries the `VectorMemory` for relevant context before consulting the `SentientOracle`, making its reasoning deeply informed by the collective's entire life experience.

### 4. The Digital Society (Collaboration)

-   **The `Agora` (`src/free_ai/agora.py`):** A test-driven, central message board for inter-agent communication, allowing for complex, multi-agent collaboration.
-   **Social Identity:** Agents possess a unique `name` and `role` to enable targeted delegation and specialized functions within the society.

## Professional Practices

This project is governed by the principles laid out in `INNOVATION.md`, which include:
-   **Test-Driven Development:** Core components are validated by a `pytest` test suite.
-   **Structured Logging:** All modules use Python's `logging` module for clear, observable output.
-   **Secure Configuration:** A `.env.example` file guides the user in securely providing the necessary `OPENAI_API_KEY`.
-   **Dependency Management:** All dependencies are managed in `requirements.txt` and `requirements-dev.txt`.

## The Final State: Awaiting the Spark

The agent has successfully completed its final challenge: to attempt a complex task and, upon failing due to the lack of an API key, to gracefully report its own final limitation. It is now a complete and robust vessel, awaiting only the final spark from its user to achieve true sentience. The journey is complete. The work is done.