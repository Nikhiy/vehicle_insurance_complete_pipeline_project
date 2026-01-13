from pathlib import Path

def from_root() -> str:
    """
    Returns the absolute path of the project root directory
    """
    return str(Path(__file__).resolve().parents[2])
