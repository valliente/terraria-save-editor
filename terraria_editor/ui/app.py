import customtkinter as ctk
from ..parser import PLRFileHandler
from ..models import Player
from .file_tab import FileTab
from .stats_tab import StatsTab
from .inventory_tab import InventoryTab
from .journey_tab import JourneyTab

class TerrariaSaveEditorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Terraria Save Editor v2.0")
        self.geometry("1100x720")
        self.minsize(950, 650)
        self.configure(fg_color="#121212")

        # Set Dark Mode Theme
        ctk.set_appearance_mode("dark")
        
        # We will use custom colors matching the dark & emerald theme
        self.bg_color = "#121212"
        self.accent_color = "#1DB954"
        self.frame_bg = "#1A1A1A"
        self.hover_color = "#158C3E"

        self.handler = PLRFileHandler()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.frames = {}
        self.current_frame = None

        self._build_sidebar()
        self._build_main_area()
        
        # Start by showing File Management so user can load a save
        self.select_tab("File Management")

    def _build_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        self.sidebar_frame.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        title_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Terraria Save Editor v2.0", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.accent_color
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        # Navigation Buttons
        self.nav_buttons = {}
        
        nav_items = [
            ("Player Data", "Player Data", True),
            ("Inventory", "Inventory", True),
            ("Journey & Buffs", "Journey & Buffs", True),
            ("File Management", "File Management", True),
            ("Settings", "Settings", False)
        ]
        
        for idx, (btn_text, tab_name, enabled) in enumerate(nav_items, start=1):
            cmd = (lambda name=tab_name: self.select_tab(name)) if enabled else None
            btn = ctk.CTkButton(
                self.sidebar_frame, 
                text=btn_text, 
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w",
                fg_color="transparent",
                text_color="#FFFFFF" if enabled else "#555555",
                hover_color=self.hover_color if enabled else self.frame_bg,
                border_spacing=10,
                command=cmd
            )
            btn.grid(row=idx, column=0, padx=10, pady=5, sticky="ew")
            self.nav_buttons[tab_name] = btn

        # Status area at the bottom left
        self.status_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="#222222", corner_radius=8)
        self.status_frame.grid(row=7, column=0, padx=10, pady=20, sticky="ew")
        
        self.status_title = ctk.CTkLabel(self.status_frame, text="Current Save:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#AAAAAA", anchor="w")
        self.status_title.pack(padx=10, pady=(10, 0), fill="x")
        
        self.status_text = ctk.CTkLabel(self.status_frame, text="None", font=ctk.CTkFont(size=10), text_color="#666666", anchor="w", justify="left")
        self.status_text.pack(padx=10, pady=(0, 10), fill="x")

    def _build_main_area(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, padx=(10, 15), pady=15, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.frames["File Management"] = FileTab(
            self.main_container,
            handler=self.handler,
            on_player_loaded_callback=self._on_player_loaded,
            on_log_callback=self._log,
            on_sync_data_callback=self._on_data_changed
        )
        
        self.frames["Player Data"] = StatsTab(
            self.main_container,
            on_data_changed_callback=self._on_data_changed
        )
        
        self.frames["Inventory"] = InventoryTab(
            self.main_container,
            on_data_changed_callback=self._on_data_changed
        )
        
        self.frames["Journey & Buffs"] = JourneyTab(
            self.main_container,
            on_data_changed_callback=self._on_data_changed
        )

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_remove()

    def select_tab(self, name):
        # Update button colors
        for btn_name, btn in self.nav_buttons.items():
            if btn.cget("state") != "disabled" and btn.cget("text_color") != "#555555":
                btn.configure(fg_color="transparent", text_color="#FFFFFF", border_color=self.frame_bg, border_width=0)
        
        if name in self.nav_buttons:
            self.nav_buttons[name].configure(fg_color="#181818", text_color=self.accent_color, border_color=self.accent_color, border_width=1)

        # Show frame
        if name in self.frames:
            if self.current_frame:
                self.current_frame.grid_remove()
            self.current_frame = self.frames[name]
            self.current_frame.grid()

    def _on_player_loaded(self, player: Player):
        file_path = self.handler.current_file_path
        # Truncate path if too long
        display_path = file_path if len(file_path) < 40 else "..." + file_path[-37:]
        self.status_text.configure(text=display_path, text_color=self.accent_color)
        
        self.stats_tab.load_player_data(player)
        self.inventory_tab.load_player_data(player)
        self.frames["Journey & Buffs"].load_player_data(player)

    @property
    def stats_tab(self):
        return self.frames["Player Data"]
        
    @property
    def inventory_tab(self):
        return self.frames["Inventory"]
        
    def _on_data_changed(self):
        if self.handler.player:
            self.stats_tab.apply_to_player()
            self.inventory_tab.apply_to_player()
            self.frames["Journey & Buffs"].apply_to_player()

    def _log(self, msg: str):
        if hasattr(self.frames["File Management"], 'write_log'):
            self.frames["File Management"].write_log(msg)
