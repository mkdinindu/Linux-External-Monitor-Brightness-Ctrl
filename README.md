# Brightness Controller for Linux

A lightweight Linux tray application for controlling external monitor brightness using DDC/CI and `ddcutil`.

Built with:
- Python
- GTK3
- AppIndicator
- ddcutil

## Features

- Tray icon
- External monitor auto detection
- Brightness sliders
- Multi-monitor support
- Startup service support
- Lightweight and native Linux UI

## Requirements

Install dependencies:

```bash
sudo apt install python3 python3-pip ddcutil \
python3-gi gir1.2-gtk-3.0 \
gir1.2-appindicator3-0.1
```

## Important

Enable DDC/CI in your monitor settings.

Most monitors have:
- Settings
- System
- DDC/CI → ON

Laptop internal displays do not support DDC/CI.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/brightness-controller-linux.git
cd brightness-controller-linux
```

Run:

```bash
python3 main.py
```

---


## Screenshots

### System top tray bar
<img width="255" alt="System tray" src="https://github.com/user-attachments/assets/fd196535-1338-432b-a919-c8a013cea588" />

### Drop down menu
<img width="290" alt="Dropdown menu" src="https://github.com/user-attachments/assets/66222a81-1d16-4f2c-8e3e-53573f4bfde6" />

### Brightness control window
<img width="326" alt="Brightness control" src="https://github.com/user-attachments/assets/26f0d8fc-bf2c-4420-a61b-c66b0d6513ce" />


## Startup Service

Example user service:

```ini
[Unit]
Description=Brightness Controller Tray App

[Service]
ExecStart=/usr/bin/python3 /path/to/main.py
Restart=always

[Install]
WantedBy=default.target
```

Enable:

```bash
systemctl --user daemon-reload
systemctl --user enable brightness-controller.service
systemctl --user start brightness-controller.service
```

---

## Known Issues

- Some monitors respond slowly to DDC commands
- NVIDIA drivers may interfere with DDC
- USB-C docks may block I2C communication
- GNOME may require AppIndicator extension

---

## Future Plans

- Better UI
- Brightness presets
- Wayland support improvements
- Hotkeys
- OSD overlay
- Auto brightness

---

## License

MIT License
