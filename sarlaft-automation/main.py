import argparse
from pathlib import Path
from src.pipeline import process_case


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inbox", default="data/inbox", help="Carpeta con subcarpetas por cédula")
    parser.add_argument("--out", default="output/alertas.xlsx")
    args = parser.parse_args()

    inbox = Path(args.inbox)
    for case_dir in sorted(p for p in inbox.iterdir() if p.is_dir()):
        print(f"Procesando {case_dir.name}...")
        case = process_case(case_dir, args.out)
        print(f"  -> {case.analisis_generado[:80]}...")


if __name__ == "__main__":
    main()
