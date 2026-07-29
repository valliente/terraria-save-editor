import customtkinter as ctk
from ..parser import PLRFileHandler
from ..models import Player
from .file_tab import FileTab
from .stats_tab import StatsTab
from .inventory_tab import InventoryTab
from .journey_tab import JourneyTab
from .banner_tab import BannerTab
from .world_tab import WorldTab

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
        
        # Bind hotkeys
        self.bind("<Control-o>", lambda e: self.frames["File Management"]._browse_file())
        self.bind("<Control-s>", lambda e: self.frames["File Management"]._save_file())
        self.bind("<Control-z>", self._on_undo)
        
    def _on_undo(self, event=None):
        if self.current_frame == self.frames.get("Inventory"):
            self.frames["Inventory"]._clear_slot()
        # Add other undo logic for active frame if needed

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
            ("World Editing", "World", False),
            ("Player Data", "Player Data", False),
            ("Inventory", "Inventory", False),
            ("Journey & Buffs", "Journey & Buffs", False),
            ("Banner Management", "Banner Management", False),
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
            on_player_loaded_callback=None, # Overridden
            on_log_callback=self._log,
            on_sync_data_callback=self._on_data_changed
        )
        self.frames["File Management"].on_data_loaded = self._on_data_loaded
        
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

        self.frames["Banner Management"] = BannerTab(
            self.main_container,
            on_data_changed_callback=self._on_data_changed
        )

        self.frames["World"] = WorldTab(
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

    def _on_data_loaded(self, data, file_path):
        display_path = file_path if len(file_path) < 40 else "..." + file_path[-37:]
        self.status_text.configure(text=display_path, text_color=self.accent_color)
        
        is_world = file_path.endswith(".wld") or ".wld.bak" in file_path
        
        # Toggle Navigation visibility
        for btn_name, btn in self.nav_buttons.items():
            if btn_name in ["File Management", "Settings"]: continue
            if is_world:
                state = "normal" if btn_name == "World" else "disabled"
            else:
                state = "disabled" if btn_name == "World" else "normal"
                
            btn.configure(state=state, text_color="#FFFFFF" if state=="normal" else "#555555")
            if state == "disabled" and self.current_frame == self.frames[btn_name]:
                self.select_tab("File Management")
        
        if is_world:
            self.frames["World"].load_world_data(data)
            self.select_tab("World")
        else:
            self.stats_tab.load_player_data(data)
            self.inventory_tab.load_player_data(data)
            self.frames["Journey & Buffs"].load_player_data(data)
            self.frames["Banner Management"].load_player_data(data)
            self.select_tab("Player Data")

    @property
    def stats_tab(self):
        return self.frames["Player Data"]
        
    @property
    def inventory_tab(self):
        return self.frames["Inventory"]
        
    def _on_data_changed(self):
        if hasattr(self.handler, 'player') and self.handler.player:
            self.stats_tab.apply_to_player()
            self.inventory_tab.apply_to_player()
            self.frames["Journey & Buffs"].apply_to_player()
            self.frames["Banner Management"].apply_to_player()
            
        wld_handler = getattr(self.frames["File Management"], 'wld_handler', None)
        if wld_handler and wld_handler.world:
            self.frames["World"].apply_to_world()

    def _log(self, msg: str):
        if hasattr(self.frames["File Management"], 'write_log'):
            self.frames["File Management"].write_log(msg)
