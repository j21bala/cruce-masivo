from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class AlertCase:
    cedula: str
    nombre: str

    actividad_economica: str = ""
    nivel_riesgo_actividad: str = ""
    condicion_pep: str = "NO"
    fecha_actualizacion: str = ""
    productos: str = ""
    fecha_apertura: str = ""
    oficina: str = ""
    movimientos: str = ""
    saldo: str = ""
    perfil_transaccional_acorde: str = "SI"
    monto_efectivo_acorde: str = "SI"
    jurisdiccion_habitual: str = "SI"
    canal_habitual: str = "SI"
    cliente_alertado_antes: str = "NO"
    se_solicitaron_soportes: str = "NO"
    resultado_soportes: str = ""
    hallazgos: str = ""
    motivo_alerta: str = ""
    conclusion: str = ""
    imagenes_faltantes: str = ""

    analisis_generado: str = ""
    fecha_procesamiento: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def to_dict(self) -> dict:
        return asdict(self)

    def variables_para_prompt(self) -> dict:
        """Solo las variables que tienen valor (las vacías se omiten en el prompt)."""
        d = self.to_dict()
        skip = {"analisis_generado", "fecha_procesamiento"}
        return {k: v for k, v in d.items() if k not in skip and v}
