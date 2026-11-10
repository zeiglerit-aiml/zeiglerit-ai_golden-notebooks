# Golden Jupyter Notebook Collection

A collection of reusable notebooks and hands-on ML demonstrations.

## Tracked notebooks

- `notebooks/exploratory_end_to_end_ml_pipeline.ipynb` — end-to-end exploratory machine-learning and model-serving pipeline demonstration, including prediction and related use cases.
- `notebooks/ml_landscape_all.ipynb` — three independent interactive dropdowns for Machine Learning Algorithms, Neural Network Algorithms, and AI Algorithms. Each selection displays context, use cases, and a practical Python snippet; the detailed reference lessons remain below.
- `notebooks/advanced_ai_algorithms.ipynb` — 12 additional AI algorithm lessons from PPO and A* through MCTS, LSTMs, DNC, alpha-beta pruning, YOLO, GANs, VGG/ResNet, behavior trees, SAC, and self-/cross-attention, with Python examples and production-scope notes.

## Notebook validation

The maintained notebooks are stored individually under `notebooks/`; duplicate packaged snapshots are not retained. GitHub Actions validates notebook structure and Python syntax. Interactive selectors require `ipywidgets`; optional YOLO examples require `ultralytics`. Before running optional model downloads, inspect the selected checkpoint and source. Use a clean environment and trusted datasets.

## Portfolio ownership

Canonical home for maintained notebook source. Packaged ZIPs are archival snapshots until extracted, reviewed, and validated.

Account-wide ownership and cleanup decisions are maintained in the [WSP portfolio repository catalog](https://github.com/zeiglerit-aiml/WSP_Integrated_AI_SDLC_GVC_pl/blob/main/REPOSITORY_CATALOG.md).
