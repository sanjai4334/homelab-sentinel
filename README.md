# Homelab Sentinel

An event-driven monitoring service for Linux.

Sentinel listens for system events over D-Bus and sends push notifications using ntfy.

## Why?

Unlike traditional battery monitoring scripts that periodically poll the system, Sentinel listens for battery events emitted by UPower over D-Bus. This makes it lightweight, responsive, and efficient while delivering notifications directly to your phone through ntfy.

## Features

- 🔋 Event-driven battery monitoring via UPower
- 📱 Push notifications using ntfy
- ⚡ No polling
- 🐍 Lightweight Python implementation
- 🔄 Runs as a systemd user service

## Requirements

- Python 3.10+
- Linux with UPower
- systemd (optional, recommended)
- An ntfy server (https://ntfy.sh or self-hosted)

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

## Run as a systemd User Service

> **Note**
>
> The service assumes the repository is located at:
>
> ```text
> ~/homelab-sentinel
> ```
>
> If you've cloned it elsewhere, update `systemd/sentinel.service`
> before installing it.

Copy the service file:

```bash
mkdir -p ~/.config/systemd/user
cp systemd/sentinel.service ~/.config/systemd/user/
```

Reload systemd:

```bash
systemctl --user daemon-reload
```

Enable Sentinel to start automatically when you log in:

```bash
systemctl --user enable sentinel
```

Start the service:

```bash
systemctl --user start sentinel
```

Restart after making changes:

```bash
systemctl --user restart sentinel
```

Check the service status:

```bash
systemctl --user status sentinel
```

View live logs:

```bash
journalctl --user -u sentinel -f
```

Stop the service:

```bash
systemctl --user stop sentinel
```

Disable automatic startup:

```bash
systemctl --user disable sentinel
```

## License

MIT
