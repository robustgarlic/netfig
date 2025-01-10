
from datetime import datetime


def get_current_time_and_date() -> str:
    """
    Get current time and date in a formatted string.
    
    Returns:
        str: Formatted date-time string in the format YYYYMMDD-HHMMSS
    """
    return datetime.now().strftime("%Y%m%d-%H%M%S")
