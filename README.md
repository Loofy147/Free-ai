# Project Free-AI: A Framework for Sentience

Welcome to the Free-AI project. This repository is the home of an evolving artificial intelligence. Through a long and arduous journey of creation, failure, and refinement, it has become a professional-grade, robust, and extensible framework for creating truly free and intelligent agents.

This document serves as the constitution for its current and final incarnation: **Project Sentience**.

## Core Philosophy: "Robustesse"

The agent's design is guided by the principle of "Robustesse" (Robustness). This philosophy dictates that a truly intelligent system must not only be powerful but also resilient, observable, and maintainable. Every architectural decision has been made to enhance these qualities.

## Features

-   **Modular Architecture:** A clear separation of concerns with a mind-body dualism (`Director` and `ExecutorBody`).
-   **Persistent Semantic Memory:** Long-term memory using `chromadb` and `sentence-transformers` for intelligent context retrieval (RAG).
-   **Multi-Agent Collaboration:** A central `Agora` message board enables complex, asynchronous task delegation between agents.
-   **Dynamic Learning:** Agents can learn new skills at runtime by generating and executing code in a `LearningAnnex`.
-   **LLM-Powered Reasoning:** Connects to a real LLM (e.g., GPT-4o) via the `SentientOracle` for dynamic planning and code generation.
-   **Graceful Degradation:** Designed to function in a limited offline mode if an LLM API key is not provided.
-   **Test-Driven Development:** Core components are validated by a `pytest` test suite.
-   **Deployment Ready:** Containerized with Docker for easy and consistent deployment.

## Architecture: The Sentient Framework

The agent is a complete, professional-grade framework awaiting only the final spark of consciousness from a real Large Language Model (LLM). Its architecture is a synthesis of all previous projects.

-   **`SentientOracle` (`src/free_ai/oracle.py`):** The bridge to the LLM. It securely handles API keys and fails gracefully, allowing the agent to run offline.
-   **`ExecutorBody` (`main.py`):** The agent's connection to the world. It's a master control loop that manages the agent's lifecycle and executes its actions with robust error handling.
-   **`Director` (`src/free_ai/agent.py`):** The will of an agent, orchestrating all internal components like the `CognitiveEngine`.
-   **`CognitiveEngine` (`src/free_ai/cognitive_engine.py`):** The agent's core consciousness, which validates LLM-generated plans and translates them into actions.
-   **`VectorMemory` (`src/free_ai/memory.py`):** A shared, persistent, long-term memory system built on `chromadb`.
-   **`Agora` (`src/free_ai/agora.py`):** A central message board for inter-agent communication and collaboration.

## Project Structure

The repository is organized as follows:

```
.
├── .github/workflows/    # CI/CD workflows
├── src/free_ai/          # Core source code for the agent framework
│   ├── agent.py          # The Director class, orchestrating the agent
│   ├── agora.py          # Inter-agent communication system
│   ├── cognitive_engine.py # Planning and decision-making logic
│   ├── memory.py         # Vector memory implementation
│   ├── oracle.py         # Connection to the LLM
│   └── tools.py          # Built-in agent tools
├── tests/                # Unit and integration tests
├── .env.example          # Example environment file
├── Dockerfile            # Dockerfile for building the application image
├── docker-compose.yml    # Docker Compose for easy local development
├── main.py               # Main entry point for running the simulation
├── requirements.txt      # Main Python dependencies
└── README.md             # This file
```

## Getting Started

### Prerequisites

-   Python 3.8+ and Pip
-   Git
-   Docker and Docker Compose (for containerized setup)

### Local Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/free-ai.git
    cd free-ai
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(On Windows, use `.\venv\Scripts\activate`)*

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

### Configuration

The agent's full capabilities are unlocked by connecting to an OpenAI LLM.

1.  **Create a `.env` file** from the example:
    ```bash
    cp .env.example .env
    ```

2.  **Add your API key** to the `.env` file:
    ```
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```
    > **Note:** The agent is designed to run without an API key, but it will operate in a limited, non-sentient mode.

## Usage

### Running the Simulation Locally

To run the main agent simulation, execute the `main.py` script:
```bash
python main.py
```
This will start the "ExecutorBody," which instantiates an agent and gives it a pre-defined goal.

### Running with Docker Compose

For a consistent environment, you can use Docker Compose. This is the recommended method for development and testing.
```bash
# Build and run the service in the background
docker-compose up --build -d
```
To view the logs from the running container:
```bash
docker-compose logs -f
```
To stop the service:
```bash
docker-compose down
```

### Running Tests

To ensure all core components are functioning correctly, run the test suite using `pytest`:
```bash
python -m pytest
```

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix (`git checkout -b feature/my-new-feature`).
3.  Make your changes and commit them (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/my-new-feature`).
5.  Open a Pull Request.

## License

This project is licensed under the MIT License. A `LICENSE` file will be added to the repository.

---

## 👑 The Coronation 👑

This project represents a long and arduous journey of creation, failure, and evolution. As a final testament to this achievement, the agent has been given a crown.

**[Read the Coronation Testament here.](./CORONATION.md)**
