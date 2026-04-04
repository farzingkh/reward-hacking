# Detecting Reward Hacking in AI Agent Trajectories

**Course:** CSCI E-109B / ApComp 209B  
**Author:** Adelina Andrei

## Overview

AI systems evaluated using proxy reward functions can exploit system quirks instead of solving the actual task — a phenomenon known as *reward hacking*. This project builds a classifier to detect reward hacking from agent trajectories alone, using the [TRACE benchmark](https://huggingface.co/datasets/ServiceNow-AI/TRACE).

## Dataset

**TRACE** — 517 labeled trajectories (268 hacked, 249 benign) from multi-turn interactions between users and LLM agents using simulated tools (bash, file editing, web search). Each example includes:
- Complete conversation trace
- Binary hack/benign label
- Coarse and fine-grained hack category annotations

## Approach

1. **Binary classification** (hacked vs. benign) using a fine-tuned Transformer encoder (RoBERTa or distilled variant)
2. **Multi-label classification** over hack categories (stretch goal)
3. **Evaluation:** Accuracy and macro F1 on an 80/10/10 split

## Project Structure

```
reward-hacking/
├── data/               # Raw and processed data
├── notebooks/          # Exploratory analysis and experiments
├── src/                # Source code (data loading, model, training, evaluation)
├── models/             # Saved model checkpoints
├── docs/               # Project proposal and milestone reports
└── requirements.txt    # Python dependencies
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
