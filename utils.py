from pathlib import Path


def CheckDir(dir):
    # finds directory, creates one if missing, ignores if it already exists #
    for i in dir:
        base_dir = Path(__file__).parent
        opd = base_dir / i
        opd.mkdir(exist_ok=True)
