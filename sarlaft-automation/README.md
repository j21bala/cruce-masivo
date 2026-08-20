# sarlaft-automation

Pipeline semanal para procesar alertas SARLAFT a partir de capturas de pantalla.

- OCR local (Tesseract) para extraer campos de las capturas -> NO usa LLM (costo ~0).
- Un único llamado a LLM por caso, solo para redactar el párrafo final de análisis.
- Salida a Excel/SQLite como fuente para Power BI.

## Flujo
1. Analista deja las imágenes de un caso en `data/inbox/<cedula>/`.
2. `main.py` clasifica cada imagen por tipo de pantalla (nombre de archivo o heurística).
3. `src/ocr` extrae texto y lo parsea a campos estructurados (regex por tipo de pantalla).
4. `src/llm/generator.py` arma el prompt (`prompts/analisis_sarlaft.txt`) con esos campos y hace UNA llamada al LLM.
5. `src/storage.py` guarda el registro en `output/alertas.xlsx` (o SQLite).
6. Power BI se conecta a `output/alertas.xlsx` / la base y refresca.

## Setup
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# Tesseract debe estar instalado en el sistema (apt install tesseract-ocr / choco install tesseract)
```

## Uso
```bash
python main.py --inbox data/inbox --out output/alertas.xlsx
```
