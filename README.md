# Terraria Save File Editor 🗡️

A modern, local desktop application for editing Terraria player save files (`.plr`) on Windows.

![Terraria Save Editor](https://img.shields.io/badge/Platform-Windows-blue)
![Version](https://img.shields.io/badge/Release-v1.0.0-success)

---

## 🌟 Features

- **🔒 AES Decryption & Encryption**: Seamlessly decrypts and re-encrypts `.plr` files using AES-128-CBC.
- **🛡️ Auto-Backup System**: Automatically creates a `<filename>.plr.bak` backup file before writing any changes to disk.
- **👤 Player Attribute Editor**: Modify Player Name, Difficulty Mode (*Classic, Mediumcore, Hardcore, Journey*), Max & Current Health (*up to 500 HP*), Max & Current Mana (*up to 200 Mana*), Hair Style, and Hex/RGB Colors.
- **🎒 Inventory Editor**:
  - Edit all 50 main inventory slots + 8 Coin & Ammo slots.
  - Searchable Item Presets (*Zenith, Terraprisma, Platinum Coins, Life Crystal, Solar Armor, etc.*).
  - Modifier & Prefix selector (*Legendary, Unreal, Mythical, Godly, Warding, Menacing, etc.*).
  - One-click presets: *Give 9999 Platinum Coins*, *Add Endgame Starter Pack*.
- **📁 File Management**: Auto-locates standard Terraria player save directories (`My Games\Terraria\Players`) and supports quick backup restoration.

---

## 🚀 Download & Installation

1. Go to the [Releases](https://github.com/valliente/terraria-save-editor/releases) page.
2. Download `TerrariaSaveEditor.exe`.
3. Double-click `TerrariaSaveEditor.exe` to run (no Python installation or dependencies required).

---

## 💻 Building from Source

```bash
# Clone the repository
git clone https://github.com/valliente/terraria-save-editor.git
cd terraria-save-editor

# Install dependencies
pip install customtkinter pycryptodome pyinstaller

# Run locally
python main.py

# Build single-file standalone executable
pyinstaller --noconsole --onefile --collect-all customtkinter --name="TerrariaSaveEditor" main.py
```

---

## 📄 License

MIT License. Free to use and modify for personal non-commercial use.
