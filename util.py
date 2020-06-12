from pathlib import Path


def nr2str(int):
    return str(int).zfill(3)


def is_packaged():
    "If bundled the file requirements.txt is not included."
    if (Path(__file__).parent / 'requirements.txt').exists():
        return False
    else:
        return True
