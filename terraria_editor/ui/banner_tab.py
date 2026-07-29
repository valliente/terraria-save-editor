import customtkinter as ctk
from ..models import Player

class BannerTab(ctk.CTkFrame):
    def __init__(self, parent, on_data_changed_callback):
        super().__init__(parent, fg_color="transparent")
        self.on_data_changed = on_data_changed_callback
        self.player: Player = None

        self.accent_color = "#1DB954"
        self.frame_bg = "#1A1A1A"
        self.input_bg = "#222222"

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build_ui()

    def _build_ui(self):
        # Header
        header_card = ctk.CTkFrame(self, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        header_card.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="ew")
        
        ctk.CTkLabel(header_card, text="🎏 Banner Management", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.accent_color).pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(header_card, text="Manage monster kill counts and unlock banner claims directly from the save.", font=ctk.CTkFont(size=12), text_color="#AAAAAA").pack(anchor="w", padx=15, pady=(0, 15))

        # Main List Area
        list_card = ctk.CTkFrame(self, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        list_card.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        list_card.grid_columnconfigure(0, weight=1)
        list_card.grid_rowconfigure(2, weight=1)

        # Search Bar
        search_f = ctk.CTkFrame(list_card, fg_color="transparent")
        search_f.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        search_f.grid_columnconfigure(0, weight=1)

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_f, textvariable=self.search_var, placeholder_text="Search for monsters...", fg_color=self.input_bg, border_color=self.accent_color, border_width=1, text_color="#FFFFFF", height=35)
        search_entry.grid(row=0, column=0, sticky="ew")

        ctk.CTkButton(search_f, text="Unlock All Banners", font=ctk.CTkFont(weight="bold"), fg_color=self.input_bg, hover_color="#333333", border_color=self.accent_color, border_width=1, text_color="#FFFFFF", height=35).grid(row=0, column=1, padx=(10, 0))

        # Warning
        ctk.CTkLabel(list_card, text="⚠️ Note: 1.4.5 Banner mapping is pending API updates. This UI is visually complete but backend binary serialization is blocked to prevent .plr corruption.", text_color="#E5C07B", font=ctk.CTkFont(size=11, slant="italic")).grid(row=1, column=0, padx=15, sticky="w")

        # Scrollable Grid
        scroll = ctk.CTkScrollableFrame(list_card, fg_color="transparent")
        scroll.grid(row=2, column=0, padx=10, pady=(10, 15), sticky="nsew")
        scroll.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Mock list of monsters
        monsters = ["Blue Slime", "Green Slime", "Zombie", "Demon Eye", "Skeleton", "Cave Bat", "Piranha", "Devourer", "Face Monster", "Crimera", "Bunny", "Goldfish", "Voodoo Demon", "Bone Serpent", "Hornet", "Man Eater"]

        for i, monster in enumerate(monsters):
            row = i // 4
            col = i % 4
            
            f = ctk.CTkFrame(scroll, fg_color=self.input_bg, border_color="#333333", border_width=1, corner_radius=6)
            f.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            ctk.CTkLabel(f, text=monster, font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFFFFF").pack(anchor="w", padx=10, pady=(10, 2))
            
            # Kills input
            k_f = ctk.CTkFrame(f, fg_color="transparent")
            k_f.pack(fill="x", padx=10, pady=(0, 10))
            ctk.CTkLabel(k_f, text="Kills:", font=ctk.CTkFont(size=11), text_color="#AAAAAA").pack(side="left")
            entry = ctk.CTkEntry(k_f, width=50, height=24, fg_color="#111111", border_color="#333333", border_width=1, text_color=self.accent_color)
            entry.insert(0, "0")
            entry.pack(side="left", padx=5)

    def load_player_data(self, player: Player):
        self.player = player

    def apply_to_player(self) -> Player:
        return self.player
