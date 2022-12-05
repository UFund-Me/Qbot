from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.joinpath("gui")

DATA_DIR_CSV = DATA_DIR.joinpath("csv")
DATA_DIR_BKT_RESULT = DATA_DIR.joinpath("bkt_result")

dirs = [DATA_DIR, DATA_DIR_CSV, DATA_DIR_BKT_RESULT]
for dir in dirs:
    dir.mkdir(exist_ok=True, parents=True)
