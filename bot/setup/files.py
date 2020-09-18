from pathlib import Path

def create_dirs():
    Path('./out').mkdir(exist_ok=True)
    Path('./out/profiles').mkdir(exist_ok=True)
    Path('./out/logs').mkdir(exist_ok=True)