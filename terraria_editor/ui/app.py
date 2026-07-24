import customtkinter as ctk
from ..parser import PLRFileHandler
from ..models import Player
from .file_tab import FileTab
from .stats_tab import StatsTab
from .inventory_tab import InventoryTab

class TerrariaSaveEditorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Terraria Save File Editor v1.0.0")
        self.geometry("1100x720")
        self.minsize(950, 650)

        # Set Dark Mode Theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.handler = PLRFileHandler()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_tabs()

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#11111B", height=60)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)

        # Logo & App Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🗡️ Terraria Save Editor",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#89B4FA"
        )
        title_label.grid(row=0, column=0, padx=20, pady=12, sticky="w")

        # Current Player Status Badge
        self.status_badge = ctk.CTkLabel(
            header_frame,
            text="Status: No File Loaded",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#A6ADC8",
            fg_color="#1E1E2E",
            corner_radius=8,
            padx=12,
            pady=6
        )
        self.status_badge.grid(row=0, column=2, padx=20, pady=12, sticky="e")

    def _build_tabs(self):
        self.tabview = ctk.CTkTabview(self, corner_radius=10, fg_color="#181825")
        self.tabview.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="nsew")

        tab_file = self.tabview.add("File Management")
        tab_stats = self.tabview.add("Player Stats")
        tab_inventory = self.tabview.add("Inventory Editor")

        # File Tab
        self.file_tab = FileTab(
            tab_file,
            handler=self.handler,
            on_player_loaded_callback=self._on_player_loaded,
            on_log_callback=self._log
        )
        self.file_tab.pack(fill="both", expand=True)

        # Stats Tab
        self.stats_tab = StatsTab(
            tab_stats,
            on_data_changed_callback=self._on_data_changed
        )
        self.stats_tab.pack(fill="both", expand=True)

        # Inventory Tab
        self.inventory_tab = InventoryTab(
            tab_inventory,
            on_data_changed_callback=self._on_data_changed
        )
        self.inventory_tab.pack(fill="both", expand=True)

    def _on_player_loaded(self, player: Player):
        self.status_badge.configure(
            text=f"Loaded: {player.name} (HP: {player.hp}/{player.max_hp})",
            text_color="#A6E3A1",
            fg_color="#313244"
        )
        self.stats_tab.load_player_data(player)
        self.inventory_tab.load_player_data(player)

    def _on_data_changed(self):
        if self.handler.player:
            self.stats_tab.apply_to_player()
            self.inventory_tab.apply_to_player()

    def _log(self, msg: str):
        if hasattr(self, 'file_tab'):
            self.file_tab.write_log(msg)
