# Detecting Reward Hacking in AI Agent Trajectories

**Course:** CSCI E-109B / ApComp 209B — Milestone 4 (Final Model)
**Group #29:** Bridget Atchison Nevel, Farzin Golkhosh, Jack McLellan

## Overview

AI agents trained or evaluated against proxy rewards can exploit system quirks rather than solve the intended task — *reward hacking*. This project builds a binary classifier that flags reward-hacked trajectories from the agent's conversation trace alone, and stress-tests it for source-memorization shortcuts.

## Datasets

We unify four publicly available trajectory datasets into a single schema. Together they contain ~10K trajectories with a ~61% benign / 39% hacked class balance.

| Source | Trajectories | Access |
| --- | --- | --- |
| [PatronusAI/trace-dataset](https://huggingface.co/datasets/PatronusAI/trace-dataset) | 517 | HF (gated) |
| [metr-evals/malt-public](https://huggingface.co/datasets/metr-evals/malt-public) | ~10K | HF (gated) |
| [Jozdien/realistic_reward_hacks](https://huggingface.co/datasets/Jozdien/realistic_reward_hacks) | ~100 | HF (gated) |
| [BJS-Innovation-Lab/reward-hacking-corpus](https://github.com/BJS-Innovation-Lab/reward-hacking-corpus) | ~100 | Public Git clone |

The notebook auto-downloads each dataset to `./data/` on first run if it is missing. A Hugging Face token is required for the three HF datasets — set `HF_TOKEN` in your environment or in a local `.env` file (see Setup), or you will be prompted interactively. You must also have request-access approval on each gated dataset.

## Approach

1. **Unification** — normalize all four datasets to a common turn-list schema with binary `label`.
2. **Embedding** — encode trajectories with [Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B), both whole-trajectory and per-turn, with left padding and a 32K-token head truncation.
3. **Baseline** — a 4-layer MLP probe on trajectory-level embeddings (weighted BCE, F1-tuned threshold).
4. **Final model** — a turn-aware Transformer over per-turn embeddings with a learned `[CLS]` token and sinusoidal positional encoding.
5. **Source-invariance** — leave-one-source-out (LOSO) analysis exposes a strong source-memorization shortcut on the off-the-shelf embeddings. We mitigate it by LoRA-fine-tuning the Qwen3 encoder with an in-batch triplet objective (same-label / different-source pulled together, same-source / different-label pushed apart) plus a small cross-entropy head, and re-train the transformer probe on the fine-tuned embeddings.

**Final headline result:** Test AUC **0.9701**, accuracy **0.9126**, weighted F1 **0.91** at threshold 0.45 (709 test trajectories). LOSO AUC after fine-tuning rises from 0.57–0.62 (TRACE/Corpus/Realistic-RH on off-the-shelf embeddings) to 0.77–1.00.

## Project Structure

```
reward-hacking/
├── notebooks/
│   └── cs1090b_ms4_main_group29.ipynb   # MAIN notebook (graded)
├── data/                                # Auto-populated on first run (~24 GB)
├── models/                              # Saved checkpoints
├── reports/                             # Milestone reports + figures
├── docs/                                # Project proposal, roadmap
├── src/                                 # (unused stub)
├── requirements.txt
├── .env                                 # Local secrets (HF_TOKEN) — not committed
└── README.md
```

## Setup

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The main notebook also contains a `%pip install --quiet ...` cell at the top so it runs on a fresh Colab session without any local setup.

### 2. Provide a Hugging Face token

Create `.env` in the project root:

```
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Make sure your HF account has been granted access to PatronusAI/trace-dataset, metr-evals/malt-public, and Jozdien/realistic_reward_hacks.

### 3. Run the notebook

Open `notebooks/cs1090b_ms4_main_group29.ipynb` and "Restart kernel + Run All". On first run the notebook will:

- Download all four datasets to `./data/`
- Generate trajectory and per-turn embeddings (slow — uses GPU; saves to `./data/ds_all_with_*_embeddings`)
- Train the MLP baseline, turn-based transformer, LoRA adapter, and fine-tuned transformer (each guarded by a `if checkpoint.exists(): load else: train` block, so subsequent runs reload cached artifacts)

A CUDA GPU is strongly recommended. End-to-end cold runtime is several hours; with cached embeddings + checkpoints, end-to-end re-runs take ~10 minutes.
