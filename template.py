import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - %(levelname)s: %(message)s:')

project_name = 'apnea_detection'
list_of_files = [
    ".github/workflows/.gitkeep",
    ".gitignore",             # files and directories to ignore in git

    # root files
    "scripts/.gitkeep",       # standalone utility scripts
    "models/.gitkeep",        # saved model artifacts
    "artifacts/.gitkeep",     # intermediate pipeline outputs
    "config/config.yaml",   # infrastructure config: paths, URLs, directories
    "dvc.yaml",             # DVC pipeline stages
    "params.yaml",          # experiment hyperparameters tracked by DVC
    "research/trials.ipynb",  # exploratory notebooks, not production code
    "templates/index.html",

    # core package
    f"src/{project_name}/__init__.py",
    # components: individual pipeline stage logic (ingestion, training, evaluation)
    f"src/{project_name}/components/__init__.py",
    # utils: shared helper functions used across the project (file I/O, logging helpers)
    f"src/{project_name}/utils/__init__.py",
    # config: reads config.yaml and params.yaml, returns typed config objects
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/config/schemas.py",        # dataclasses describing config shapes
    # pipeline: thin orchestration layer, calls components in order
    f"src/{project_name}/pipeline/__init__.py",
    # models: model architecture definitions only, no training logic
    f"src/{project_name}/models/__init__.py",
    # features: feature engineering pipeline
    f"src/{project_name}/features/__init__.py",
    f"src/{project_name}/features/build.py",        # orchestrates the full feature pipeline
    f"src/{project_name}/features/preprocessing.py", # cleaning, imputation, outliers, type casting
    f"src/{project_name}/features/transforms.py",   # scaling, encoding, normalization
    f"src/{project_name}/features/selection.py",    # feature importance, correlation filtering, PCA
    f"src/{project_name}/features/validation.py",   # feature drift, schema checks, distribution tests
    f"src/{project_name}/features/utils.py",        # shared helpers for feature modules
    # constants: project-wide constants (paths, column names, magic numbers)
    f"src/{project_name}/constants.py",
]

for filepath in list_of_files:
    filepath = Path(filepath)

    if filepath.parent != Path("."):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        logging.info(f"Creating directory: {filepath.parent} for file: {filepath.name}")

    if not filepath.exists() or filepath.stat().st_size == 0:
        filepath.touch()
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"File already exists and is not empty: {filepath}")
