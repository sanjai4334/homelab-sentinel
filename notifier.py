from dotenv import load_dotenv
from os import getenv
import requests

load_dotenv()

NTFY_SERVER = getenv("NTFY_SERVER")
NTFY_TOPIC = getenv("NTFY_TOPIC")
URL = f"{NTFY_SERVER}/{NTFY_TOPIC}"


def notify(
    title: str, message: str, priority: str | None = None, tags: list[str] | None = None
) -> None:

    headers = {"Title": title}

    if priority:
        headers["Priority"] = priority

    if tags:
        headers["Tags"] = ",".join(tags)

    response = requests.post(
        URL,
        data=message,
        headers=headers,
        timeout=10,
    )

    response.raise_for_status()


if __name__ == "__main__":
    notify("Test notification", "This is a test notification from sentinel.")
