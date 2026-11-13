# Agentic AI Systems Engineering — Week 05

## Project Overview

This repository contains the practical implementations and experiments completed during **Week 05 of Agentic AI Systems Engineering**.

The project explores core concepts of building reliable agentic AI systems using Python and a locally running Large Language Model (LLM) through Ollama.

The practical examples use an insurance claim processing scenario to demonstrate prompt engineering, evaluation, validation, workflow management, context handling, and agentic decision-making.

## Technology Stack

- **Programming Language:** Python
- **LLM Runtime:** Ollama
- **LLM Model:** Qwen 2.5 (7B)
- **Environment:** Python Virtual Environment
- **Libraries:** Python dependencies listed in `requirements.txt`

## Topics Covered

The project is organized into eight modules:

| Folder | Topic | Description |
|---|---|---|
| `01_prompt_engineering` | Prompt Engineering | Role-based prompts, constraints, and structured instructions. |
| `02_prompt_evaluation` | Prompt Evaluation | Comparing prompts, temperature settings, zero-shot and few-shot approaches, and evaluation metrics. |
| `03_output_validation` | Output Validation | Validating LLM responses, bounded retries, and evaluator-optimizer patterns. |
| `04_loop_engineering` | Loop Engineering | State machines, execution budgets, retries, and backoff strategies. |
| `05_prompt_chaining` | Prompt Chaining | Breaking complex tasks into sequential prompts and using critique-and-revision workflows. |
| `06_context_engineering` | Context Engineering | Comparing relevant and irrelevant context and evaluating its effect on model performance. |
| `07_agentic_workflows` | Agentic Workflows | Building workflows where an agent selects actions based on the current state. |
| `08_observability` | Observability | Monitoring execution, tracking latency, recording events, and generating final reports. |

## Project Structure

```text
Week-5/
│
├── 01_prompt_engineering/
├── 02_prompt_evaluation/
├── 03_output_validation/
├── 04_loop_engineering/
├── 05_prompt_chaining/
├── 06_context_engineering/
├── 07_agentic_workflows/
├── 08_observability/
│
├── data/
├── prompts/
├── results/
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Prerequisites

Make sure the following are installed:

- Python 3.10 or later
- Ollama
- Git (optional)

## Setup and Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_FOLDER
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Download the Ollama model

Make sure Ollama is installed and running, then execute:

```powershell
ollama pull qwen2.5:7b
```

### 6. Run an example

For example:

```powershell
python .\07_agentic_workflows\agent_workflow.py
```

You can execute other Python files inside their respective topic folders.

## Learning Outcomes

Through these practical implementations, the project demonstrates:

- Designing effective prompts for LLM-based applications.
- Evaluating model responses and prompt performance.
- Implementing output validation and bounded retry mechanisms.
- Managing execution loops and workflow states.
- Breaking complex tasks into manageable prompt chains.
- Providing relevant context to improve model responses.
- Implementing action-selection logic in agentic workflows.
- Tracking model latency, execution attempts, and workflow events.

## Practical Scenario

The examples use insurance claim processing as a common scenario. The system processes claims involving property damage, vehicle damage, theft, and medical expenses.

The scenario provides a consistent way to experiment with LLM behavior, structured outputs, validation, and autonomous workflow decisions.

## Author

**Hasnain Ahmed Ansari**

BS Computer Science — Mohammad Ali Jinnah University (MAJU)

GitHub: YOUR_GITHUB_PROFILE_URL

