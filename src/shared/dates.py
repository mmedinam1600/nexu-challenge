from datetime import datetime
from zoneinfo import ZoneInfo
from core.config import settings


def now() -> datetime:
    """
    Devuelve la fecha y hora actual con la zona horaria definida en la configuración.
    """
    return datetime.now(ZoneInfo(settings.TIME_ZONE))
