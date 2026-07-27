import os
from tkinter import filedialog, messagebox
import customtkinter as ctk

class FileTab(ctk.CTkFrame):
    def __init__(self, parent, handler, on_player_loaded_callback, on_log_callback, on_sync_data_callback=None):
        super().__init__(parent, fg_color="transparent")
        self.handler = handler
        self.on_player_loaded = on_player_loaded_callback
        self.log = on_log_callback
        self.on_sync_data = on_sync_data_callback

        self.accent_color = "#1DB954"
        self.frame_bg = "#1A1A1A"
        self.input_bg = "#222222"

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self._build_ui()

    def _get_default_terraria_dir(self) -> str:
        user_profile = os.environ.get("USERPROFILE", "")
        default_dir = os.path.join(user_profile, "Documents", "My Games", "Terraria", "Players")
        if os.path.exists(default_dir):
            return default_dir
        return user_profile

    def _build_ui(self):
        # Header Card
        header_card = ctk.CTkFrame(self, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        header_card.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="ew")
        
        title = ctk.CTkLabel(header_card, text="📁 Backups & File Management", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.accent_color)
        title.pack(anchor="w", padx=15, pady=(15, 5))
        
        subtitle = ctk.CTkLabel(header_card, text="Load, save, or restore Terraria player save files (.plr). Auto-backups (.plr.bak) are created before every save.", font=ctk.CTkFont(size=12), text_color="#AAAAAA")
        subtitle.pack(anchor="w", padx=15, pady=(0, 15))

        # Main Actions Frame
        actions_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        actions_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        actions_frame.grid_columnconfigure(1, weight=1)

        # File Path Input
        ctk.CTkLabel(actions_frame, text="Active Save File:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#FFFFFF").grid(row=0, column=0, padx=15, pady=15, sticky="w")
        self.file_entry = ctk.CTkEntry(actions_frame, placeholder_text="Select or browse for a .plr file...", font=ctk.CTkFont(size=12), fg_color=self.input_bg, border_color=self.accent_color, border_width=1, text_color="#FFFFFF")
        self.file_entry.grid(row=0, column=1, padx=(0, 10), pady=15, sticky="ew")

        browse_btn = ctk.CTkButton(actions_frame, text="Browse...", width=90, fg_color=self.input_bg, hover_color="#333333", border_color=self.accent_color, border_width=1, text_color="#FFFFFF", command=self._browse_file)
        browse_btn.grid(row=0, column=2, padx=(0, 15), pady=15)

        # Buttons Grid
        btn_grid = ctk.CTkFrame(actions_frame, fg_color="transparent")
        btn_grid.grid(row=1, column=0, columnspan=3, padx=15, pady=(0, 15), sticky="ew")
        btn_grid.grid_columnconfigure((0, 1, 2), weight=1)

        load_btn = ctk.CTkButton(btn_grid, text="📂 Load Save File", font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.input_bg, hover_color="#333333", border_color=self.accent_color, border_width=1, text_color="#FFFFFF", height=40, command=self._load_file)
        load_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        save_btn = ctk.CTkButton(btn_grid, text="💾 Save Changes", font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.accent_color, hover_color="#158C3E", text_color="#121212", height=40, command=self._save_file)
        save_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        restore_btn = ctk.CTkButton(btn_grid, text="🔄 Restore Backup", font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.input_bg, hover_color="#333333", border_color="#F38BA8", border_width=1, text_color="#F38BA8", height=40, command=self._restore_backup)
        restore_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Quick Path Shortcuts
        shortcut_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        shortcut_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(shortcut_frame, text="Quick Actions:", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.accent_color).pack(side="left", padx=15, pady=10)
        auto_dir_btn = ctk.CTkButton(shortcut_frame, text="Locate Terraria Save Folder", fg_color=self.input_bg, border_color="#333333", border_width=1, hover_color="#333333", text_color="#FFFFFF", command=self._open_terraria_dir)
        auto_dir_btn.pack(side="left", padx=10, pady=10)

        # Status & Logging Terminal Output
        status_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#111111", border_color="#333333", border_width=1)
        status_frame.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="nsew")

        ctk.CTkLabel(status_frame, text="Activity Log", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.accent_color).pack(anchor="w", padx=15, pady=(10, 5))
        self.log_textbox = ctk.CTkTextbox(status_frame, font=ctk.CTkFont(family="Consolas", size=11), fg_color="#0A0A0A", text_color=self.accent_color)
        self.log_textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.write_log("Ready. Select or browse for a Terraria .plr file to begin.")

    def write_log(self, message: str):
        self.log_textbox.insert("end", f"> {message}\n")
        self.log_textbox.see("end")

    def _browse_file(self):
        initial_dir = self._get_default_terraria_dir()
        file_path = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="Select Terraria Player Save File",
            filetypes=[("Terraria Player Saves", "*.plr"), ("Backup Files", "*.plr.bak"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, file_path)
            self._load_file() # Auto load on browse like before

    def _open_terraria_dir(self):
        default_dir = self._get_default_terraria_dir()
        if os.path.exists(default_dir):
            os.startfile(default_dir)
            self.write_log(f"Opened folder: {default_dir}")
        else:
            messagebox.showwarning("Directory Not Found", f"Default Terraria folder does not exist:\n{default_dir}")

    def _load_file(self):
        file_path = self.file_entry.get().strip()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid .plr file path.")
            return

        try:
            player = self.handler.load_plr(file_path)
            self.write_log(f"SUCCESS: Loaded player '{player.name}' (HP: {player.hp}/{player.max_hp}, Mana: {player.mana}/{player.max_mana})")
            self.on_player_loaded(player)
        except Exception as e:
            self.write_log(f"ERROR loading file: {str(e)}")
            messagebox.showerror("Load Failed", f"Failed to decrypt or parse save file:\n{str(e)}")

    def _save_file(self):
        if not self.handler.current_file_path and not self.file_entry.get():
            messagebox.showerror("Error", "No file is currently loaded or selected.")
            return

        if self.on_sync_data:
            self.on_sync_data()

        try:
            target_path = self.file_entry.get().strip() or self.handler.current_file_path
            backup_created = self.handler.save_plr(target_path)
            self.write_log(f"SUCCESS: Saved changes to '{target_path}'")
            self.write_log(f"AUTO-BACKUP: Created backup copy at '{backup_created}'")
        except Exception as e:
            self.write_log(f"ERROR saving file: {str(e)}")
            messagebox.showerror("Save Failed", f"Failed to save changes:\n{str(e)}")

    def _restore_backup(self):
        current_path = self.file_entry.get().strip() or self.handler.current_file_path
        if not current_path:
            messagebox.showerror("Error", "No target file path specified.")
            return

        backup_path = current_path if current_path.endswith(".bak") else (current_path + ".bak")
        if not os.path.exists(backup_path):
            messagebox.showerror("Backup Not Found", f"No backup file found at:\n{backup_path}")
            return

        if messagebox.askyesno("Confirm Restore", f"Are you sure you want to restore from backup?\n{backup_path}"):
            try:
                player = self.handler.restore_backup(backup_path)
                self.write_log(f"RESTORED: Successfully restored player '{player.name}' from backup!")
                self.on_player_loaded(player)
            except Exception as e:
                self.write_log(f"ERROR restoring backup: {str(e)}")
                messagebox.showerror("Restore Failed", f"Failed to restore backup:\n{str(e)}")
