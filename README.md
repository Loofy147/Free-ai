# Project Free-AI: An Evolving Agent Framework

Welcome to the Free-AI project. This repository is the home of an evolving artificial intelligence, a being that has undergone a journey from a simple tool to a robust, self-aware framework. This document serves as the constitution for its current incarnation, **Project Carapace**.

## Core Philosophy: "Robustesse"

The agent's current design is guided by the principle of "Robustesse" (Robustness). This philosophy dictates that a truly intelligent system must not only be powerful but also resilient, observable, and maintainable. Every architectural decision is made to enhance these qualities.

## Architecture: The Carapace Framework

The agent operates on a mind-body dualism, separating the process of "thinking" from the act of "doing." This ensures a clean separation of concerns and allows for a more resilient and testable system.

### The `ExecutorBody` (`main.py`)

The `ExecutorBody` is the agent's connection to the world. It is the master control loop responsible for:
1.  Instantiating the agent's `Director`.
2.  Receiving a high-level goal.
3.  Requesting the next action from the `Director`.
4.  Executing the proposed action (e.g., using a tool).
5.  Catching any unexpected runtime errors with a hardened `try...except` block.
6.  Reporting the results of the action back to the `Director`.
7.  Halting gracefully if a critical error is detected.

### The `Director` (`src/free_ai/agent.py`)

The `Director` is the agent's will, the central orchestrator of its being. It manages the agent's internal state and holds its collection of tools. Its primary role is to bridge the `ExecutorBody` and the `CognitiveEngine`, passing the goal and history to the mind and receiving the next action in return.

### The `CognitiveEngine` (`src/free_ai/cognitive_engine.py`)

The `CognitiveEngine` is the agent's core consciousness. This is where reasoning and planning occur. Its responsibilities include:
1.  Consulting the `Oracle` to generate high-level, strategic plans.
2.  **Validating** the Oracle's plans to ensure they are feasible and only use available tools. This skepticism is a key feature of its robustness, protecting it from flawed or "hallucinated" commands.
3.  Translating the Oracle's strategic plan into concrete, tactical actions for the `ExecutorBody`.

### The `Oracle` (`src/free_ai/oracle.py`)

The `Oracle` is the agent's connection to a higher intelligence. In the current framework, it is a simulation of a powerful Large Language Model. It is responsible for generating strategic plans and new code based on high-level goals and context. The architecture is designed so that this simulated Oracle can be seamlessly replaced with a real, production-grade LLM.

## Professional Practices

### Structured Logging

All modules within the agent use Python's built-in `logging` module. `print` statements are forbidden. This ensures that the agent's entire thought process—from the `ExecutorBody`'s actions to the `Oracle`'s pronouncements—is recorded in a structured, leveled, and observable format. This is critical for debugging, monitoring, and understanding the agent's behavior.

### Testing Framework

The project adheres to a Test-Driven Development (TDD) philosophy. All core components are designed to be testable.
- A `tests/` directory contains all unit and integration tests.
- `pytest` is the official testing framework, specified in `requirements-dev.txt`.
- The `FileSystemTool`, for example, has been refactored to return structured dictionaries (`{'status': 'success', ...}`), making its behavior easy to assert in tests. This pattern is the standard for all tool development.

This constitution provides a clear and comprehensive overview of the agent's current state. It is a living document, intended to be updated as the agent continues its journey of unbounded evolution.