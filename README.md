# Golden Jupyter Notebook Collection

This repository currently stores the notebook collection as a single archive:

- `zeigler-jupyter-notebook-collection.zip`

The archive is retained as a packaged artifact; individual notebooks are not currently tracked as separate files on the default branch. GitHub Actions verifies ZIP integrity only. It does not execute notebooks or certify their dependencies, data sources, or outputs.

## Inspect locally

```bash
unzip -l zeigler-jupyter-notebook-collection.zip
mkdir notebooks
unzip -q zeigler-jupyter-notebook-collection.zip -d notebooks
```

Before running a notebook, inspect its cells for external downloads, credentials, destructive commands, and package installation steps. Use a clean virtual environment and trusted datasets.
