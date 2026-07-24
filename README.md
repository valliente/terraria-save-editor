# Terraria Save File Editor 🗡️

A modern, local desktop application for editing Terraria player save files (`.plr`) on Windows.

![Terraria Save Editor](https://img.shields.io/badge/Platform-Windows-blue)
![Version](https://img.shields.io/badge/Release-v1.0.0-success)

---

## 🛡️ Windows SmartScreen / Defender Notice

Because this is a standalone open-source utility compiled with PyInstaller, Windows SmartScreen or Smart App Control may display an *"Unknown Publisher"* warning upon downloading or launching for the first time.

### How to run smoothly:

- **Option A (Quick UI Unblock)**:
  1. Click **More info** on the blue SmartScreen prompt.
  2. Click **Run anyway**.

- **Option B (Unblock File Properties)**:
  1. Right-click `TerrariaSaveEditor.exe` -> **Properties**.
  2. At the bottom of the **General** tab, check **Unblock** -> **Apply**.

- **Option C (PowerShell One-Liner)**:
  ```powershell
  Unblock-File -Path .\TerrariaSaveEditor.exe
  ```

---

## 🌟 Features

- **🔒 AES Decryption & Encryption**: Decrypts and re-encrypts `.plr` files using AES-128-CBC.
- **🛡️ Auto-Backup System**: Automatically creates a `<filename>.plr.bak` backup copy before writing changes.
- **👤 Player Attribute Editor**: Modify Name, Difficulty Mode (*Classic, Mediumcore, Hardcore, Journey*), Health (*100-500 HP*), Mana (*20-200 Mana*), Hair Style, and Hex/RGB Colors.
- **🎒 Inventory Editor**:
  - Interactive grid for all 50 main inventory slots + 8 Coin & Ammo slots.
  - Searchable Item Presets (*Zenith, Terraprisma, Platinum Coins, Solar Armor, etc.*).
  - Modifier & Prefix selector (*Legendary, Unreal, Mythical, Godly, Warding, Menacing, etc.*).
  - One-click presets: *Give 9999 Platinum Coins*, *Add Endgame Starter Pack*.
- **📁 File Management**: Auto-locates standard Terraria player save directories (`My Games\Terraria\Players`) and supports quick backup restoration.

---

## 🚀 Download & Installation

1. Go to the [Releases](https://github.com/valliente/terraria-save-editor/releases) page.
2. Download `TerrariaSaveEditor.exe`.
3. Unblock the file (if prompted by SmartScreen) and double-click to launch!

---

## 💻 Building from Source

```bash
# Clone repository
git clone https://github.com/valliente/terraria-save-editor.git
cd terraria-save-editor

# Install dependencies
pip install customtkinter pycryptodome pyinstaller

# Run locally
python main.py

# Build single-file executable
pyinstaller --noconsole --onefile --collect-all customtkinter --name="TerrariaSaveEditor" main.py
```

---

## 📄 License

MIT License. Free to use and modify.
