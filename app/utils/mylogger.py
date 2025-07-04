import os
from datetime import datetime, timezone

LOG_FILE_PATH = "../../logs/error_log.txt"

def log_error(error_code: str, error_message: str, context: str = ""):
    """
    Logs an error with timestamp, error code, and message into a text file.
    
    Args:
        error_code (str): Custom or standard error code (e.g., '500', 'FOREIGN_KEY_VIOLATION').
        error_message (str): Human-readable error message.
        context (str): Optional additional context (e.g., function name or module).
    """
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    log_entry = (
        f"\n----- ERROR LOG -----\n"
        f"Timestamp : {timestamp}\n"
        f"Error Code: {error_code}\n"
        f"Context   : {context}\n"
        f"Message   : {error_message}\n"
        f"----------------------\n"
    )

    with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)