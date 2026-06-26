# Homelab Sentinel

An event-driven monitoring service for Linux.

Sentinel listens to system events over D-Bus and sends notifications to your phone using ntfy.

## Features

-   🔋 Battery monitoring via UPower
-   📱 Push notifications using ntfy
-   ⚡ Event-driven (no polling)
-   🐍 Lightweight Python implementation

## Requirements

-   Python 3.10+
-   Linux with UPower
-   An ntfy server (https://ntfy.sh or self-hosted)

## Installation

Clone the repository:

```bash
git clone https://github.com/sanjai4334/homelab-sentinel.git
cd homelab-sentinel
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

### Linux/macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```env
NTFY_SERVER=https://ntfy.sh
NTFY_TOPIC=your-random-uuid-topic
```

## Running

```bash
python main.py
```
