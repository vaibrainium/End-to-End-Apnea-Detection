import os
from box.exceptions import BoxValueError
import yaml
from cnn_classifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any, List
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its contents as a ConfigBox object.

    Args:
        path_to_yaml (Path): The path to the YAML file.
    Returns:
        ConfigBox: The contents of the YAML file as a ConfigBox object.
    Raises:
        BoxValueError: If the YAML file is empty or cannot be parsed.
        e: empty or invalid YAML file
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError as e:
        raise BoxValueError(f"YAML file: {path_to_yaml} is empty or cannot be parsed. Error: {e}")
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Creates directories if they do not exist.

    Args:
        path_to_directories (List[Path]): A list of paths to the directories to be created.
        verbose (bool, optional): If True, logs the creation of each directory. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Directory created at: {path}")

def save_json(path: Path, data: Any):
    """
    Saves data to a JSON file.

    Args:
        path (Path): The path to the JSON file where the data will be saved.
        data (Any): The data to be saved in the JSON file.
    """
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    logger.info(f"Data saved to JSON file at: {path}")

def load_json(path: Path) -> Any:
    """
    Loads data from a JSON file.

    Args:
        path (Path): The path to the JSON file from which the data will be loaded.
    Returns:
        Any: The data loaded from the JSON file.
    """
    with open(path, "r") as json_file:
        content = json.load(json_file)
    logger.info(f"Data loaded from JSON file at: {path}")
    return ConfigBox(content)

def save_bin(data: Any, path: Path):
    """
    Saves data to a binary file using joblib.

    Args:
        data (Any): The data to be saved in the binary file.
        path (Path): The path to the binary file where the data will be saved.
    """
    joblib.dump(data, path)
    logger.info(f"Data saved to binary file at: {path}")

def load_bin(path: Path) -> Any:
    """
    Loads data from a binary file using joblib.

    Args:
        path (Path): The path to the binary file from which the data will be loaded.
    Returns:
        Any: The data loaded from the binary file.
    """
    data = joblib.load(path)
    logger.info(f"Data loaded from binary file at: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """
    Gets the size of a file in a human-readable format.

    Args:
        path (Path): The path to the file whose size is to be determined.
    Returns:
        str: The size of the file in a human-readable format.
    """
    size_in_bytes = os.path.getsize(path)
    size_in_kb = size_in_bytes / 1024
    size_in_mb = size_in_kb / 1024
    if size_in_mb >= 1:
        return f"{size_in_mb:.2f} MB"
    elif size_in_kb >= 1:
        return f"{size_in_kb:.2f} KB"
    else:
        return f"{size_in_bytes} bytes"

def decode_image(img_string, filename):
    """
    Decodes a base64 encoded image string and saves it to a file.

    Args:
        img_string (str): The base64 encoded image string.
        filename (str): The name of the file where the decoded image will be saved.
    """
    img_data = base64.b64decode(img_string)
    with open(filename, 'wb') as f:
        f.write(img_data)
    logger.info(f"Image decoded and saved to: {filename}")

def encode_image_to_base64(image_path: Path) -> str:
    """
    Encodes an image file to a base64 string.

    Args:
        image_path (Path): The path to the image file to be encoded.
    Returns:
        str: The base64 encoded string of the image.
    """
    with open(image_path, "rb") as img_file:
        img_string = base64.b64encode(img_file.read()).decode('utf-8')
    logger.info(f"Image at {image_path} encoded to base64 string")
    return img_string
