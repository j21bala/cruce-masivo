from pathlib import Path
from src.ocr.extractor import extract_text
from src.ocr.parsers import parse_image
from src.llm.generator import generate_analysis
from src.models import AlertCase
from src.storage import append_case


def process_case(case_dir: Path, out_path: str):
    """case_dir: carpeta con las imágenes de UN cliente/alerta. Cero llamadas LLM aquí,
    todas las imágenes se procesan con OCR local."""
    cedula = case_dir.name
    case = AlertCase(cedula=cedula, nombre="")

    for image_path in sorted(case_dir.glob("*.*")):
        ocr_text = extract_text(str(image_path))
        screen_type, fields = parse_image(str(image_path), ocr_text)
        if not screen_type:
            continue
        for k, v in fields.items():
            if hasattr(case, k) and v:
                setattr(case, k, v)

    # Único punto donde se gasta token: redactar el párrafo final.
    case.analisis_generado = generate_analysis(case.variables_para_prompt())

    append_case(case, out_path)
    return case
