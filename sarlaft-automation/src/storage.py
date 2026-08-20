import pandas as pd
from pathlib import Path
from src.models import AlertCase


def append_case(case: AlertCase, out_path: str):
    row = case.to_dict()
    out_file = Path(out_path)
    if out_file.exists():
        df = pd.read_excel(out_file)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])
    out_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(out_file, index=False)
