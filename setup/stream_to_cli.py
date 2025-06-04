import json
import time
import sys
from datetime import datetime

def get_timestamp():
    return datetime.now().strftime("[%H:%M:%S]")

def stream_to_cli(data, delay=0.01):
    """
    Streams any data to the CLI as a string, one character at a time,
    prefixing the entire output with a single timestamp.

    Args:
        data: str, dict, list, or any object convertible to string
        delay: float, delay in seconds between characters
    """
    try:
        if isinstance(data, (dict, list)):
            string_data = json.dumps(data, indent=2)
        else:
            string_data = str(data)

        # Print timestamp once
        print(get_timestamp(), end=' ', flush=True)

        for char in string_data:
            print(char, end='', flush=True)
            time.sleep(delay)

        print()  # newline after done
    except Exception as e:
        print(f"\n[stream_to_cli error] {e}", file=sys.stderr)
