from pathlib import Path

def create_output_dirs():
    # Create output directories
    Path('./out').mkdir(exist_ok=True)
    Path('./out/profiles').mkdir(exist_ok=True)