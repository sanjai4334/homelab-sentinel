from dotenv import load_dotenv
from os import getenv
import requests

load_dotenv()

NTFY_SERVER = getenv("NTFY_SERVER")
NTFY_TOPIC = getenv("NTFY_TOPIC")
URL = f"{NTFY_SERVER}/{NTFY_TOPIC}"


def notify(title: str, message: str) -> None:

    response = requests.post(
        URL,
        data=message,
        headers={
            "Title": title,
            # "Priority": "urgent",
            # "Tags": "warning",
        },
        timeout=10,
    )

    response.raise_for_status()


if __name__ == "__main__":
    notify("Test notification", "This is a test notification from sentinel.")
