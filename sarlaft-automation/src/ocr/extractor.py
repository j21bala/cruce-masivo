import cv2
import pytesseract


def preprocess(image_path: str):
    """Mejora contraste/escala para OCR de capturas de sistemas (texto pequeño)."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def extract_text(image_path: str, lang: str = "spa") -> str:
    processed = preprocess(image_path)
    return pytesseract.image_to_string(processed, lang=lang)
