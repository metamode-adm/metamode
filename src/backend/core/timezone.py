import pytz
from datetime import datetime
from src.backend.core.config import settings

def convert_to_local_timezone(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.utc) 
    local_timezone = pytz.timezone(settings.DEFAULT_TIMEZONE)
    return dt.astimezone(local_timezone)
