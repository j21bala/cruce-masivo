from pathlib import Path
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from src.ocr.extractor import extract_text
from src.ocr.parsers import parse_fields
from src.llm.generator import generate_analysis
from src.models import AlertCase
from src.storage import append_case

app = Flask(__name__)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
OUT_PATH = "output/alertas.xlsx"

SLOTS = [
    ("inclusion_lista", "Inclusión | Lista de reserva"),
    ("datos_generales_banco", "Banco | Consulta de datos generales"),
    ("productos", "Productos del cliente"),
    ("ficha_fiduciaria", "Fiduciaria | Consulta detallada de cliente"),
    ("movimientos", "Movimientos del cliente"),
    ("saldo", "Saldo del cliente"),
]


@app.route("/")
def index():
    return render_template("index.html", slots=SLOTS)


@app.route("/procesar", methods=["POST"])
def procesar():
    cedula = request.form.get("cedula", "").strip()
    nombre = request.form.get("nombre", "").strip()
    case = AlertCase(cedula=cedula, nombre=nombre)

    case_dir = UPLOAD_DIR / cedula
    case_dir.mkdir(parents=True, exist_ok=True)

    faltantes = []
    for slot_key, slot_label in SLOTS:
        file = request.files.get(slot_key)
        if file and file.filename:
            filename = secure_filename(f"{slot_key}_{file.filename}")
            path = case_dir / filename
            file.save(path)
            ocr_text = extract_text(str(path))
            fields = parse_fields(slot_key, ocr_text)
            for k, v in fields.items():
                if hasattr(case, k) and v:
                    setattr(case, k, v)
        else:
            justificacion = request.form.get(f"justificacion_{slot_key}", "").strip()
            faltantes.append((slot_label, justificacion or "Sin justificación registrada"))

    if faltantes:
        case.imagenes_faltantes = "; ".join(f"{label}: {motivo}" for label, motivo in faltantes)

    case.analisis_generado = generate_analysis(case.variables_para_prompt())
    append_case(case, OUT_PATH)

    return render_template("resultado.html", case=case, faltantes=faltantes)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
