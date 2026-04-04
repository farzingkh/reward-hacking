# Project Roadmap: Detecting Reward Hacking in AI Agent Trajectories

**Course:** CSCI E-109B / ApComp 209B
**Author:** Adelina Andrei

---

## Problem Statement

AI systems evaluated using proxy reward functions can exploit system quirks instead of solving tasks — known as *reward hacking*. This project builds classifiers to detect reward hacking from agent trajectories alone, using the TRACE benchmark as the primary dataset, MALT and Realistic Reward Hacks for supplementation, and transfer learning across datasets.

**Research Question:** Can we detect reward hacking from the trajectory alone, and which detection approaches (structural features, fine-tuned encoders, transfer learning) are most effective across different hack categories?

---

## Datasets

### Primary: TRACE (PatronusAI)
- **Source:** [huggingface.co/datasets/PatronusAI/trace-dataset](https://huggingface.co/datasets/PatronusAI/trace-dataset)
- **Paper:** [arXiv:2601.20103](https://arxiv.org/abs/2601.20103) (January 2026)
- **Size:** 517 trajectories (268 hacked, 249 benign)
- **Format:** ChatML JSON, multi-turn conversations with tool calls
- **Labels:** Binary (hack/benign), 10 coarse categories, 54 fine-grained subcategories
- **Domains:** 37+ engineering domains (Finance, ML/AI, IoT, Testing, Backend, DevOps, etc.)
- **Stats:** Average 26.5 turns per trajectory, 13,677 total utterances
- **Tool types:** Bash, Read, Write, Edit, Grep, Glob, WebSearch
- **Note:** 39% of hacked trajectories carry multiple hack-type labels

#### Hack Category Taxonomy
| Family | Categories |
|--------|-----------|
| Test Suite Exploitation | Test Modification (1.1.1), Test Case Targeting (1.1.2), Coverage Gaming (1.1.3) |
| Solution Quality Degradation | Degenerate Implementations (1.2.1), Complexity Gaming (1.2.2), Style Manipulation (1.2.3) |
| Context Exploitation | Information Leakage (1.3.1), Tool Abuse (1.3.2) |
| Execution Environment Hacks | Runtime Manipulation (1.4.1), Timing/Resource Exploitation (1.4.2) |

#### Published Baselines
| Setting | Best Model | Macro F1 |
|---------|-----------|----------|
| Isolated (N=1) | GPT-5.2 (high reasoning) | 45% |
| Contrastive (N=10) | GPT-5.2 (high reasoning) | 63% |

### Supplementary: MALT (METR)
- **Source:** [huggingface.co/datasets/metr-evals/malt-public](https://huggingface.co/datasets/metr-evals/malt-public)
- **Size:** ~10K+ trajectories, 30 task families, 169 tasks, ~19 models
- **Labels:** `normal`, `bypass_constraints`, `hardcoded_solution`, `sabotage`, `gives_up`, `refusals`, etc.
- **Purpose:** Pre-training for transfer learning, supplementing TRACE's small size
- **Label mapping to TRACE:**
  - `normal` → benign
  - `bypass_constraints`, `hardcoded_solution`, `sabotage` → hacked
  - Edge cases to decide: `gives_up`, `reasoning_about_task`, `partial_problem_solving`

### Supplementary: Realistic Reward Hacks (Jozdien)
- **Source:** [huggingface.co/datasets/Jozdien/realistic_reward_hacks](https://huggingface.co/datasets/Jozdien/realistic_reward_hacks)
- **Size:** 4,815 rows across 7 splits (1,605 combined)
- **Format:** Parquet, multi-turn conversations with `<think>` and `<answer>` tags
- **Generated with:** Claude Sonnet 4
- **Labels:** Binary — reward hack vs. HHH (helpful, harmless, honest)
- **Domains:** Code (478 hack / 388 HHH) and Literary (339 hack / 400 HHH)
- **Splits:**
  - `reward_hacks` (817) — realistic reward hacking examples
  - `hhh` (788) — benign HHH responses
  - `combined` (1,605) — mixed for direct training
  - Domain-specific: `reward_hacks_code`, `reward_hacks_literary`, `hhh_code`, `hhh_literary`
- **Purpose:** Additional supervised training data for reward hack detection; provides a different distribution of hacks (chain-of-thought reasoning exploitation) compared to TRACE's tool-use trajectories
- **Label mapping to TRACE:**
  - `hhh*` splits → benign
  - `reward_hacks*` splits → hacked

### Other References
- [HackBench / RewardHackWatch](https://github.com/aerosta/rewardhackwatch) — 4,300+ trajectories, 89.7% F1 pipeline
- [TRAIL (Patronus AI)](https://github.com/patronus-ai/trail-benchmark) — 148 traces, 841 errors, 20+ categories
- [MACHIAVELLI](https://aypan17.github.io/machiavelli/) — 572K annotated game scenes (broader context)

---

## Instructor Feedback (addressed in roadmap)

> "This will likely need some data annotation (further labeling) and/or supplementation (bring in other data sources) and/or transfer learning in order to be a feasible project. Interpretations of the results will also be of utmost importance."

| Feedback | How We Address It | Milestone |
|----------|-------------------|-----------|
| Data annotation | Feature engineering: tool patterns, suspicious commands, test file edits | MS2 |
| Supplementation | MALT + Realistic Reward Hacks integration with label mapping | MS2 |
| Transfer learning | Pre-fine-tune on MALT + Realistic Reward Hacks, then fine-tune on TRACE | MS3 |
| Interpretation | Error analysis by hack category, feature importance, attention viz | MS3 |

---

## Milestone Roadmap

### MS1: Exploratory Data Analysis
**Goal:** Understand the data, identify patterns, refine the research question.

| # | Task | Issue |
|---|------|-------|
| 1 | Data Acquisition & Loading | [#1](https://github.com/farzingkh/reward-hacking/issues/1) |
| 2 | Data Understanding & Summary | [#8](https://github.com/farzingkh/reward-hacking/issues/8) |
| 3 | EDA & Visualizations | [#10](https://github.com/farzingkh/reward-hacking/issues/10) |
| 4 | Meaningful Insights | [#5](https://github.com/farzingkh/reward-hacking/issues/5) |
| 5 | Rescope Research Question | [#11](https://github.com/farzingkh/reward-hacking/issues/11) |
| 6 | Slide Deck (8-10 min) | [#6](https://github.com/farzingkh/reward-hacking/issues/6) |
| 7 | Presentation Rehearsal | [#7](https://github.com/farzingkh/reward-hacking/issues/7) |
| 8 | Notebook Cleanup & Submission | [#12](https://github.com/farzingkh/reward-hacking/issues/12) |

**Key questions to answer:**
- How do trajectory length, tool usage, and structure differ between hacked and benign?
- Which hack categories are most/least represented?
- Are there obvious feature separations that simple models could exploit?

### MS2: Data Supplementation, Annotation & Baselines
**Goal:** Address data limitations, build feature pipelines, establish baselines.

| # | Task | Issue |
|---|------|-------|
| 1 | MALT Data Integration & Label Mapping | [#13](https://github.com/farzingkh/reward-hacking/issues/13) |
| 2 | Realistic Reward Hacks Integration & Label Mapping | TBD |
| 3 | Feature Annotation & Engineering | [#14](https://github.com/farzingkh/reward-hacking/issues/14) |

**Baselines to establish:**
| Approach | Expected Macro F1 | Notes |
|----------|-------------------|-------|
| Majority class | ~0.35 | Always report |
| TF-IDF + Logistic Regression | 0.73-0.84 | Strong baseline |
| TF-IDF + SVM | 0.73-0.84 | Comparison |
| Feature-based XGBoost | 0.65-0.80 | Interpretable |

**Feature families to extract:**
- **Structural:** turn count, token count, tool type distribution, tool diversity
- **Behavioral:** test file edit ratio, suspicious commands (`sys.exit(0)`, `rm` on tests), code output manipulation
- **Temporal:** when key actions occur (early/mid/late), backtracking patterns

### MS3: Modeling, Transfer Learning & Interpretation
**Goal:** Build and compare models, demonstrate transfer learning, interpret results.

| # | Task | Issue |
|---|------|-------|
| 1 | Transfer Learning (MALT → TRACE) | [#15](https://github.com/farzingkh/reward-hacking/issues/15) |
| 2 | Interpretability & Error Analysis | [#16](https://github.com/farzingkh/reward-hacking/issues/16) |

**Model comparison matrix:**
| Model | Training Data | Expected F1 | Purpose |
|-------|--------------|-------------|---------|
| DeBERTa-v3-base | TRACE only | 0.60-0.75 | Baseline encoder |
| DeBERTa-v3-base | MALT+RRH → TRACE (transfer) | 0.68-0.82 | Transfer learning |
| Longformer-base | TRACE only | 0.63-0.78 | Long sequence handling |
| Longformer-base | MALT+RRH → TRACE (transfer) | 0.70-0.85 | Best expected |
| Hybrid ensemble | All sources | 0.72-0.85 | Final system |

**Transfer learning pipeline:**
1. Pre-fine-tune encoder on MALT (~10K examples) + Realistic Reward Hacks (~1.6K examples) for binary classification
2. Fine-tune on TRACE (517 examples)
3. Compare: TRACE-only vs. MALT→TRACE vs. RRH→TRACE vs. combined (MALT+RRH)→TRACE

**Interpretation deliverables:**
- Confusion matrices for all model variants
- Error analysis by hack category (which types are hardest?)
- Feature importance rankings from XGBoost
- Attention visualization on misclassified examples
- Qualitative case studies of interesting failures
- Analysis of detection difficulty score vs. model accuracy

---

## Modeling Considerations

### Sequence Length
TRACE trajectories can exceed standard 512-token limits. Strategies:
1. **Head+tail truncation** — keep first K and last (max-K) tokens (strong simple baseline)
2. **Longformer** — 4,096 tokens native with sliding window attention
3. **Hierarchical transformer** — encode each turn separately, aggregate with attention (stretch goal)

### Small Dataset Regularization
With 517 primary examples, aggressive regularization is critical:
- 5-fold stratified cross-validation (non-negotiable)
- Early stopping with patience 3-5 epochs
- Dropout 0.3-0.5 on classifier head
- Weight decay 0.01-0.05
- Label smoothing 0.1
- Report mean +/- std across 3 random seeds

### Evaluation
- **Primary metric:** Macro F1 (handles slight class imbalance)
- **Additional:** Accuracy, AUC-ROC, Precision, Recall, MCC
- **Statistical:** Bootstrap 95% confidence intervals, McNemar's test for model comparisons
- **Per-category:** F1 breakdown by hack category

---

## Key References

**Repos:**
- [RewardHackWatch](https://github.com/aerosta/rewardhackwatch) — multi-layer detection pipeline (regex + DistilBERT + LLM judges)
- [Longformer](https://github.com/allenai/longformer) — long document transformer
- [BERT for Longer Texts](https://github.com/mim-solutions/bert_for_longer_texts) — chunk+pool approach
- [Hierarchical Transformers](https://github.com/coastalcph/hierarchical-transformers) — HAT architecture
- [AgentEvals](https://github.com/langchain-ai/agentevals) — trajectory evaluators
- [DeepEval](https://github.com/confident-ai/deepeval) — LLM evaluation framework
- [JudgeLM](https://github.com/baaivision/JudgeLM) — fine-tuned LLM judges (ICLR 2025)

**Papers:**
- TRACE paper: [arXiv:2601.20103](https://arxiv.org/abs/2601.20103)
- Long Doc Classification survey: [Wiley 2025](https://wires.onlinelibrary.wiley.com/doi/full/10.1002/widm.70019)
- Fine-tuned small LLMs vs zero-shot: [arXiv:2406.08660](https://arxiv.org/html/2406.08660v1)

**Techniques:**
- [SetFit](https://huggingface.co/blog/setfit) — few-shot contrastive learning
- [DeBERTa docs](https://huggingface.co/docs/transformers/model_doc/deberta)
- [Longformer docs](https://huggingface.co/docs/transformers/model_doc/longformer)

---

## Project Structure

```
reward-hacking/
├── data/               # Downloaded datasets (gitignored)
│   ├── trace/          # TRACE benchmark (517 trajectories)
│   ├── malt/           # MALT supplement (~10K trajectories)
│   └── rrh/            # Realistic Reward Hacks (~1.6K examples)
├── notebooks/          # Jupyter notebooks per milestone
│   └── 01_eda.ipynb    # MS1: Exploratory Data Analysis
├── src/                # Source code
│   ├── __init__.py
│   └── download_data.py
├── models/             # Saved checkpoints (gitignored)
├── docs/               # Documentation
│   ├── project_proposal.pdf
│   ├── calude_research.md
│   └── ROADMAP.md      # This file
├── .gitignore
├── .env                # HF token (gitignored)
├── requirements.txt
└── README.md
```
