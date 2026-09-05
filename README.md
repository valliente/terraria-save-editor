# Terraria Save File Editor

> **AES-128 Binary Parser and Player Save Editor for Windows**

[![Platform](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://github.com/valliente/terraria-save-editor/releases)
[![Version](https://img.shields.io/badge/Release-v1.0.0-green.svg)](https://github.com/valliente/terraria-save-editor/releases)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A standalone desktop application for parsing, inspecting, and modifying Terraria player save files (`.plr`) on Windows.

---

## Features

- **AES Decryption & Encryption**: Handles raw `.plr` decryption and re-encryption via AES-128-CBC with integrity checking.
- **Automated Backup Protection**: Automatically generates timestamped `<filename>.plr.bak` snapshots before committing modifications to disk.
- **Player Attribute Editor**: Edit Player Name, Difficulty Mode (*Classic, Mediumcore, Hardcore, Journey*), Health (*100-500 HP*), Mana (*20-200 Mana*), Hair Style indices, and Hex/RGB color parameters.
- **Inventory & Equipment Grid**:
  - Interactive grid for all 50 primary inventory slots plus dedicated Coin and Ammo channels.
  - Searchable item database with prefix modifier assignments (*Legendary, Unreal, Mythical, Godly, Warding, Menacing*).
  - Stack count controls supporting maximum values up to 9999.
- **Directory Auto-Discovery**: Automatically locates standard player save paths (`Documents\My Games\Terraria\Players`) with manual directory browsing fallback.

---

## Windows Execution & SmartScreen Advisory

Because this open-source utility is distributed as an unsigned standalone binary compiled via PyInstaller, Windows SmartScreen or Smart App Control may display an unrecognized application prompt upon initial execution.

To unblock the executable:
- **PowerShell**:
  ```powershell
  Unblock-File -Path .\TerrariaSaveEditor.exe
  ```
- **Properties Dialog**: Right-click `TerrariaSaveEditor.exe` > **Properties** > check **Unblock** at the bottom of the General tab > **Apply**.

---

## Download & Installation

1. Navigate to the [Releases](https://github.com/valliente/terraria-save-editor/releases) page.
2. Download `TerrariaSaveEditor.exe`.
3. Launch the application and select your desired `.plr` save file.

---

## Building from Source

```bash
# Clone repository
git clone https://github.com/valliente/terraria-save-editor.git
cd terraria-save-editor

# Install dependencies
pip install customtkinter pycryptodome pyinstaller

# Run locally
python main.py

# Compile standalone single-file binary
pyinstaller --noconsole --onefile --collect-all customtkinter --name="TerrariaSaveEditor" main.py
```

---

## License

Distributed under the MIT License. See `LICENSE` for details.
