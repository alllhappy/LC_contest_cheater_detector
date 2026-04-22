#handling file paths and project root path detection

from pathlib import Path

ROOT_DIR=Path.cwd()
#testing
if __name__ == 'main':
    print(ROOT_DIR)