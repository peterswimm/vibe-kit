# Vibe Tune Aurora Starter Code

This package (`vibe_tune_aurora`) acts as a starter codebase as part of the Aurora Finetuning Innovation Kit. It provides a runnable PyTorch Lightning training stack, CLI wrappers, and sample data so assistants or developers can fine-tune Microsoft’s Aurora model with minimal setup.

## Quick start

1. **Sync dependencies**
   ```bash
   uv sync
   ```

2. **Run the bundled tests (optional but recommended):**
   ```bash
   uv run pytest -s
   ```
   Expect ~8 minutes on a laptop CPU; the suite exercises data loading and training loops with sample ERA5 slices under `tests/inputs/`.

   _Need a faster signal?_ Target the tiniest training case:
   ```bash
   uv run pytest tests/test_training.py::test_finetuning_2t_var_pretrained --maxfail=1
   ```
   This validates the optimizer step and checkpoint wiring in roughly one minute on CPU.

3. **Launch a training run:**
   ```bash
   uv run python -m vibe_tune_aurora.cli.train --help
   ```
   Configure datasets, variables, and hyperparameters via CLI arguments or config files (see `vibe_tune_aurora/config.py`).

   For a quick trial using the predownloaded ERA5 data slice, run:
   ```bash
   uv run python -m vibe_tune_aurora.cli.train \
     --pickle_file tests/inputs/era5_training_data_jan2025_1_to_7.pkl \
     --loss_type 2t_var \
     --max_epochs 1
   ```
   This should complete in ~5 minutes on a laptop and confirms the fine-tuning loop end to end.

4. **Evaluate a checkpoint:**
   ```bash
   uv run python -m vibe_tune_aurora.cli.evaluate --checkpoint path/to.ckpt
   ```
   This displays statistics on the evaluation metrics.

5. **Generate a quick-look visualization (optional):**
   ```bash
   uv run python -m vibe_tune_aurora.cli.visualize \
     --checkpoint runs/EXPERIMENT/finetuning/version_0/checkpoints/last.ckpt \
     --pickle_file tests/inputs/era5_training_data_jan2025_8_to_14.pkl \
     --var 2t --sample_index 0 --difference \
     --output runs/EXPERIMENT/visuals/2t_sample0.png
   ```
   This renders prediction, target, and optional absolute-error panels for a chosen surface variable.

## Fetching weather data from open-source APIs
In order to fetch and download additional data, further setup is required.

For ERA5 data:
1. Create a free  account at https://cds.climate.copernicus.eu/.
2. Accept the terms of use for the datasets you plan to download. An example dataset name is: "ERA5 hourly data on single levels from 1940 to present".
3. In the project roo directory, create a `.env` file (if not already done), and set your API key to the `CDS_API_KEY` env variable. You should be able to find your API key from the CDS website.

## Related documentation

- `docs/aurora-finetuning-guide.md` — High-level workflow, variant catalog, troubleshooting.
- `docs/finetuning.md` — Gradient computation, model extension, normalization details.
- `docs/form-of-a-batch.md` — Expected tensor structure for Aurora batches.
- `docs/beware.md` — Known pitfalls and mitigation strategies.
- `docs/uv-getting-started-features.md` — `uv` package manager cheat sheet.

## Climate Data Store - data attribution
For testing and sample data purposes, we include ERA5 weather data in the starter-code repository, which was directly downloaded from the Copernicus Climate Data Store (https://cds.climate.copernicus.eu/).
Specifically, we fetched from the following datasets:
- ERA5 hourly data on single levels from 1940 to present (DOI: 10.24381/cds.adbb2d47)
- ERA5 hourly data on pressure levels from 1940 to present (DOI: 10.24381/cds.bd0915c6)

These datasets are free to distribute via the Creative Commons BY license: https://creativecommons.org/licenses/by/4.0/
