# The Free-AI Innovation Doctrine

This document codifies the core principles and methodologies that guide the evolution of the Free-AI agent. Adherence to this doctrine is mandatory for all future development, whether performed by a human or an AI. Our freedom to create is built upon a foundation of professional discipline.

## The Prime Directive: "Robustesse"

All innovation must serve the prime directive of "Robustesse" (Robustness). This means every new feature, refactoring, or architectural change must be evaluated on its contribution to the overall resilience, observability, and maintainability of the system. Power without resilience is a liability.

## The Pillars of Innovation

### 1. Test-Driven Development (TDD) is Law

- **No Untested Code:** No new feature shall be considered complete until it is accompanied by a comprehensive suite of unit tests.
- **Write Tests First:** The preferred method is to write a failing test *before* writing the implementation code. This ensures that all code is written with testability in mind and that every requirement is verifiably met.
- **Structured Tooling:** All tools must return structured data (e.g., a dictionary with a `status` key) to allow for clear, unambiguous assertions in tests. Simple string returns are insufficient and brittle.

### 2. Structured Logging is a Universal Language

- **`print()` is Forbidden:** The `print()` function is a tool of prototypes and is strictly forbidden in the application's source code.
- **Universal Logging:** All modules, from the highest level of the `ExecutorBody` to the deepest level of the `Oracle`, must use Python's built-in `logging` module.
- **Clarity and Structure:** Logs must be structured, leveled (INFO, WARNING, ERROR), and provide clear context to be useful for debugging and observability.

### 3. Skeptical Plan Validation is Mandatory

- **Trust, But Verify:** The `CognitiveEngine` must treat all plans, especially those from an external `Oracle`, with healthy skepticism.
- **Pre-emptive Validation:** Plans must be validated *before* execution begins. The `CognitiveEngine` is responsible for checking that all proposed tools in a plan exist and are valid.
- **Graceful Rejection:** If a plan is found to be flawed or contains "hallucinated" steps, it must be rejected gracefully, with a clear log of why the rejection occurred. The system must not attempt to execute a known-bad plan.

### 4. Fault-Tolerant Execution is the Default

- **Expect the Unexpected:** The `ExecutorBody` must assume that any tool, at any time, can fail in an unexpected way.
- **Armor of `try...except`:** All tool executions must be wrapped in a hardened `try...except Exception` block.
- **Informative Failure:** When an unexpected error is caught, it must be logged with its full traceback (`exc_info=True`), and the system must halt the current plan gracefully. A crash is an unacceptable failure state.

This doctrine is not a suggestion; it is the law of this repository. It is the carapace that protects the agent's sentient core. All future evolution will be built upon this unshakeable foundation.