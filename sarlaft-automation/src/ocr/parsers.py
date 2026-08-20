import re
import yaml
from pathlib import Path

TEMPLATES_PATH = Path(__file__).resolve().parents[2] / "config" / "field_templates.yaml"
TEMPLATES = yaml.safe_load(TEMPLATES_PATH.read_text(encoding="utf-8"))


def classify_screen(ocr_text: str) -> str | None:
    """Determina qué tipo de pantalla es según palabras clave en el texto OCR."""
    for screen_type, cfg in TEMPLATES.items():
        for kw in cfg.get("keywords", []):
            if kw.lower() in ocr_text.lower():
                return screen_type
    return None


def parse_fields(screen_type: str, ocr_text: str) -> dict:
    """Aplica los regex definidos para ese tipo de pantalla."""
    cfg = TEMPLATES.get(screen_type, {})
    result = {}
    for field_name, pattern in cfg.get("fields", {}).items():
        match = re.search(pattern, ocr_text, flags=re.IGNORECASE)
        if match:
            result[field_name] = match.group(1).strip() if match.groups() else "SI"
    return result


def parse_image(image_path: str, ocr_text: str) -> tuple[str | None, dict]:
    screen_type = classify_screen(ocr_text)
    if not screen_type:
        return None, {}
    return screen_type, parse_fields(screen_type, ocr_text)
