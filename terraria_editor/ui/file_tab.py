import os
import glob
import threading
import time
from tkinter import filedialog, messagebox
import customtkinter as ctk
import windnd

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
        
        # Hook Drag and Drop to the parent app window
        try:
            windnd.hook_dropfiles(self.winfo_toplevel().winfo_id(), func=self._on_drop)
        except Exception:
            pass # Ignore if windnd fails

    def _on_drop(self, files):
        if files:
            path = files[0].decode("gbk", errors="ignore") if isinstance(files[0], bytes) else str(files[0])
            if path.endswith(".plr") or path.endswith(".bak") or ".bak_" in path:
                self.file_combo.set(path)
                self._load_file()
            else:
                messagebox.showerror("Invalid File", "Only .plr or .bak files are supported.")

    def _get_default_terraria_dir(self) -> str:
        user_profile = os.environ.get("USERPROFILE", "")
        default_dir = os.path.join(user_profile, "Documents", "My Games", "Terraria", "Players")
        if os.path.exists(default_dir):
            return default_dir
        return user_profile
        
    def _get_local_players(self):
        d = self._get_default_terraria_dir()
        if os.path.exists(d):
            return [f for f in glob.glob(os.path.join(d, "*.plr"))]
        return []

    def _build_ui(self):
        # Header Card
        header_card = ctk.CTkFrame(self, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        header_card.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="ew")
        
        title = ctk.CTkLabel(header_card, text="📁 Backups & File Management", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.accent_color)
        title.pack(anchor="w", padx=15, pady=(15, 5))
        
        subtitle = ctk.CTkLabel(header_card, text="Load, save, or restore Terraria player save files (.plr). Auto-backups are created before every save.\nYou can also drag-and-drop .plr files anywhere into this window.", font=ctk.CTkFont(size=12), text_color="#AAAAAA")
        subtitle.pack(anchor="w", padx=15, pady=(0, 15))

        # Main Actions Frame
        actions_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        actions_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        actions_frame.grid_columnconfigure(1, weight=1)

        # File Path Input
        ctk.CTkLabel(actions_frame, text="Active Save File:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#FFFFFF").grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        players = self._get_local_players()
        self.file_combo = ctk.CTkComboBox(actions_frame, values=players if players else ["Select or browse..."], font=ctk.CTkFont(size=12), fg_color=self.input_bg, border_color=self.accent_color, border_width=1, text_color="#FFFFFF")
        if players:
            self.file_combo.set(players[0])
            
        self.file_combo.grid(row=0, column=1, padx=(0, 10), pady=15, sticky="ew")

        browse_btn = ctk.CTkButton(actions_frame, text="Browse...", width=90, fg_color=self.input_bg, hover_color="#333333", border_color=self.accent_color, border_width=1, text_color="#FFFFFF", command=self._browse_file)
        browse_btn.grid(row=0, column=2, padx=(0, 15), pady=15)

        # Buttons Grid
        btn_grid = ctk.CTkFrame(actions_frame, fg_color="transparent")
        btn_grid.grid(row=1, column=0, columnspan=3, padx=15, pady=(0, 15), sticky="ew")
        btn_grid.grid_columnconfigure((0, 1), weight=1)

        load_btn = ctk.CTkButton(btn_grid, text="📂 Load Save File", font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.input_bg, hover_color="#333333", border_color=self.accent_color, border_width=1, text_color="#FFFFFF", height=40, command=self._load_file)
        load_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        save_btn = ctk.CTkButton(btn_grid, text="💾 Save Changes", font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.accent_color, hover_color="#158C3E", text_color="#121212", height=40, command=self._save_file)
        save_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Backup Restore Frame
        backup_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        backup_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(backup_frame, text="Restore Backup:", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.accent_color).pack(side="left", padx=15, pady=10)
        
        self.backup_combo = ctk.CTkComboBox(backup_frame, values=["No backups found"], width=350, font=ctk.CTkFont(size=11), fg_color=self.input_bg, border_color="#333333", border_width=1, text_color="#FFFFFF")
        self.backup_combo.set("No backups found")
        self.backup_combo.pack(side="left", padx=10, pady=10)
        
        refresh_btn = ctk.CTkButton(backup_frame, text="Refresh", width=60, fg_color=self.input_bg, border_color="#333333", border_width=1, hover_color="#333333", text_color="#FFFFFF", command=self._refresh_backups)
        refresh_btn.pack(side="left", padx=5)

        restore_btn = ctk.CTkButton(backup_frame, text="🔄 Restore", width=100, fg_color=self.input_bg, hover_color="#333333", border_color="#F38BA8", border_width=1, text_color="#F38BA8", command=self._restore_backup)
        restore_btn.pack(side="left", padx=10, pady=10)

        # Status & Logging Terminal Output
        status_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#111111", border_color="#333333", border_width=1)
        status_frame.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="nsew")

        ctk.CTkLabel(status_frame, text="Activity Log", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.accent_color).pack(anchor="w", padx=15, pady=(10, 5))
        self.log_textbox = ctk.CTkTextbox(status_frame, font=ctk.CTkFont(family="Consolas", size=11), fg_color="#0A0A0A", text_color=self.accent_color)
        self.log_textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.write_log("Ready. Select or drag and drop a Terraria .plr file to begin.")
        self._refresh_backups()

    def write_log(self, message: str):
        self.log_textbox.insert("end", f"> {message}\n")
        self.log_textbox.see("end")

    def _browse_file(self):
        initial_dir = self._get_default_terraria_dir()
        file_path = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="Select Terraria Player Save File",
            filetypes=[("Terraria Player Saves", "*.plr"), ("Backup Files", "*.bak*"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_combo.set(file_path)
            self._load_file()

    def _refresh_backups(self):
        target_path = self.file_combo.get().strip() or self.handler.current_file_path
        if not target_path or not os.path.exists(target_path):
            self.backup_combo.configure(values=["No backups found"])
            self.backup_combo.set("No backups found")
            return
            
        backup_dir = os.path.join(os.path.dirname(target_path), "backups")
        filename = os.path.basename(target_path)
        
        if os.path.exists(backup_dir):
            backups = glob.glob(os.path.join(backup_dir, f"{filename}.bak_*"))
            backups.sort(reverse=True) # newest first
            if backups:
                self.backup_combo.configure(values=backups)
                self.backup_combo.set(backups[0])
                return
                
        self.backup_combo.configure(values=["No backups found"])
        self.backup_combo.set("No backups found")

    def _load_file(self):
        file_path = self.file_combo.get().strip()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid file path.")
            return

        self.write_log(f"Loading '{file_path}' asynchronously...")
        threading.Thread(target=self._load_file_thread, args=(file_path,), daemon=True).start()

    def _load_file_thread(self, file_path):
        try:
            player = self.handler.load_plr(file_path)
            self.after(0, lambda: self._on_load_success(player))
        except Exception as e:
            self.after(0, lambda: self._on_load_error(str(e)))

    def _on_load_success(self, player):
        self.write_log(f"SUCCESS: Loaded player '{player.name}' (HP: {player.hp}/{player.max_hp}, Mana: {player.mana}/{player.max_mana})")
        self._refresh_backups()
        self.on_player_loaded(player)

    def _on_load_error(self, err_msg):
        self.write_log(f"ERROR loading file: {err_msg}")
        messagebox.showerror("Load Failed", f"Failed to decrypt or parse save file:\n{err_msg}")

    def _save_file(self):
        if not self.handler.current_file_path and not self.file_combo.get():
            messagebox.showerror("Error", "No file is currently loaded or selected.")
            return

        if self.on_sync_data:
            self.on_sync_data()

        target_path = self.file_combo.get().strip() or self.handler.current_file_path
        self.write_log(f"Saving changes to '{target_path}' asynchronously...")
        threading.Thread(target=self._save_file_thread, args=(target_path,), daemon=True).start()

    def _save_file_thread(self, target_path):
        try:
            backup_created = self.handler.save_plr(target_path)
            self.after(0, lambda: self._on_save_success(target_path, backup_created))
        except Exception as e:
            self.after(0, lambda: self._on_save_error(str(e)))

    def _on_save_success(self, target_path, backup_created):
        self.write_log(f"SUCCESS: Saved changes to '{target_path}'")
        self.write_log(f"AUTO-BACKUP: Created backup copy at '{backup_created}'")
        self._refresh_backups()

    def _on_save_error(self, err_msg):
        self.write_log(f"ERROR saving file: {err_msg}")
        messagebox.showerror("Save Failed", f"Failed to save changes:\n{err_msg}")

    def _restore_backup(self):
        backup_path = self.backup_combo.get().strip()
        if not backup_path or backup_path == "No backups found" or not os.path.exists(backup_path):
            messagebox.showerror("Error", "No valid backup selected.")
            return

        if messagebox.askyesno("Confirm Restore", f"Are you sure you want to restore from this backup? Current data will be overwritten."):
            try:
                player = self.handler.restore_backup(backup_path)
                self.write_log(f"RESTORED: Successfully restored player '{player.name}' from backup!")
                self._load_file() # reload the restored target file
            except Exception as e:
                self.write_log(f"ERROR restoring backup: {str(e)}")
                messagebox.showerror("Restore Failed", f"Failed to restore backup:\n{str(e)}")
