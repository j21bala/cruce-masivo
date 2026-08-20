import os
from pathlib import Path
from groq import Groq

PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "analisis_sarlaft.txt"
PROMPT_TEMPLATE = PROMPT_PATH.read_text(encoding="utf-8")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def _format_variables(variables: dict) -> str:
    return "\n".join(f"- {k}: {v}" for k, v in variables.items())


def generate_analysis(variables: dict, model: str = "llama-3.1-8b-instant") -> str:
    """Una sola llamada al LLM por caso: solo texto (gratis en Groq), nunca imágenes."""
    prompt = PROMPT_TEMPLATE.format(variables=_format_variables(variables))
    response = client.chat.completions.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()
