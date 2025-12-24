import os

def load_instruction_from_file(
    filename: str, default_instruction: str = "Default instruction"
) -> str:
    """Reads instruction text from a file relative to this script."""
    instruction = default_instruction
    try:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, "r", encoding="utf-8") as f:
            instruction = f.read()
        print(f"Loaded instruction from {filename}")
    except FileNotFoundError:
        print(f"WARNING: {filename} not found, using default instruction.")
    except Exception as e:
        print(f"Error loading instruction from {filename}: {e}")
    return instruction