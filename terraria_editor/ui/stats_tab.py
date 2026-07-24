import customtkinter as ctk
from tkinter import colorchooser
from ..models import Player, GAME_MODES, GAME_MODE_IDS, Color

class StatsTab(ctk.CTkScrollableFrame):
    def __init__(self, parent, on_data_changed_callback):
        super().__init__(parent)
        self.on_data_changed = on_data_changed_callback
        self.player: Player = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self._build_ui()

    def _build_ui(self):
        # Section 1: Core Player Identity & Game Mode
        id_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1E1E2E")
        id_frame.grid(row=0, column=0, columnspan=2, padx=15, pady=10, sticky="ew")
        id_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(id_frame, text="👤 Player Identity & Mode", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")

        # Name
        ctk.CTkLabel(id_frame, text="Player Name:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(id_frame, placeholder_text="Enter player name...", font=ctk.CTkFont(size=13))
        self.name_entry.grid(row=1, column=1, padx=(0, 15), pady=10, sticky="ew")

        # Difficulty
        ctk.CTkLabel(id_frame, text="Difficulty Mode:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=2, column=0, padx=15, pady=10, sticky="w")
        self.diff_option = ctk.CTkOptionMenu(id_frame, values=list(GAME_MODE_IDS.keys()), font=ctk.CTkFont(size=13))
        self.diff_option.grid(row=2, column=1, padx=(0, 15), pady=10, sticky="w")

        # Section 2: Health & Mana Stats
        stats_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1E1E2E")
        stats_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky="ew")
        stats_frame.grid_columnconfigure((1, 3), weight=1)

        ctk.CTkLabel(stats_frame, text="❤️ Health & Mana Attributes", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, padx=15, pady=(15, 10), sticky="w")

        # Max Health
        ctk.CTkLabel(stats_frame, text="Max Health:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self.max_hp_entry = ctk.CTkEntry(stats_frame, width=90)
        self.max_hp_entry.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        
        set_500_hp_btn = ctk.CTkButton(stats_frame, text="Max (500 HP)", width=100, fg_color="#F38BA8", hover_color="#EBA0AC", text_color="#11111B", command=lambda: self._set_stat(self.max_hp_entry, 500))
        set_500_hp_btn.grid(row=1, column=2, padx=5, pady=10)

        # Current Health
        ctk.CTkLabel(stats_frame, text="Current Health:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=1, column=3, padx=(20, 5), pady=10, sticky="w")
        self.hp_entry = ctk.CTkEntry(stats_frame, width=90)
        self.hp_entry.grid(row=1, column=4, padx=(5, 15), pady=10, sticky="w")

        # Max Mana
        ctk.CTkLabel(stats_frame, text="Max Mana:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=2, column=0, padx=15, pady=10, sticky="w")
        self.max_mana_entry = ctk.CTkEntry(stats_frame, width=90)
        self.max_mana_entry.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        set_200_mana_btn = ctk.CTkButton(stats_frame, text="Max (200 Mana)", width=100, fg_color="#89B4FA", hover_color="#74C7EC", text_color="#11111B", command=lambda: self._set_stat(self.max_mana_entry, 200))
        set_200_mana_btn.grid(row=2, column=2, padx=5, pady=10)

        # Current Mana
        ctk.CTkLabel(stats_frame, text="Current Mana:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=2, column=3, padx=(20, 5), pady=10, sticky="w")
        self.mana_entry = ctk.CTkEntry(stats_frame, width=90)
        self.mana_entry.grid(row=2, column=4, padx=(5, 15), pady=10, sticky="w")

        # Section 3: Appearance & Colors
        style_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1E1E2E")
        style_frame.grid(row=2, column=0, columnspan=2, padx=15, pady=10, sticky="ew")
        style_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(style_frame, text="🎨 Styling & Customization", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")

        # Hair Style
        ctk.CTkLabel(style_frame, text="Hair Style ID:", font=ctk.CTkFont(size=13, weight="bold")).grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self.hair_style_entry = ctk.CTkEntry(style_frame, width=90)
        self.hair_style_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Color Pickers
        self.color_widgets = {}
        colors_to_edit = [
            ("Hair Color", "hair_color"),
            ("Skin Color", "skin_color"),
            ("Eye Color", "eye_color"),
            ("Shirt Color", "shirt_color"),
            ("Undershirt Color", "undershirt_color"),
            ("Pants Color", "pants_color"),
            ("Shoe Color", "shoe_color"),
        ]

        for idx, (label_text, attr_name) in enumerate(colors_to_edit, start=2):
            ctk.CTkLabel(style_frame, text=f"{label_text}:", font=ctk.CTkFont(size=12)).grid(row=idx, column=0, padx=15, pady=5, sticky="w")
            
            sub_f = ctk.CTkFrame(style_frame, fg_color="transparent")
            sub_f.grid(row=idx, column=1, padx=10, pady=5, sticky="w")

            preview_box = ctk.CTkFrame(sub_f, width=28, height=28, corner_radius=4, fg_color="#FFFFFF")
            preview_box.pack(side="left", padx=(0, 10))

            hex_entry = ctk.CTkEntry(sub_f, width=90)
            hex_entry.pack(side="left", padx=(0, 10))

            pick_btn = ctk.CTkButton(sub_f, text="Pick...", width=65, fg_color="#313244", hover_color="#45475A", command=lambda a=attr_name, p=preview_box, e=hex_entry: self._pick_color(a, p, e))
            pick_btn.pack(side="left")

            self.color_widgets[attr_name] = (preview_box, hex_entry)

    def _set_stat(self, entry_widget, value: int):
        entry_widget.delete(0, "end")
        entry_widget.insert(0, str(value))

    def _pick_color(self, attr_name: str, preview_box, hex_entry):
        color_code = colorchooser.askcolor(title=f"Choose {attr_name.replace('_', ' ').title()}")
        if color_code and color_code[1]:
            hex_str = color_code[1]
            hex_entry.delete(0, "end")
            hex_entry.insert(0, hex_str)
            preview_box.configure(fg_color=hex_str)

    def load_player_data(self, player: Player):
        self.player = player
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, player.name)

        diff_name = GAME_MODES.get(player.difficulty, "Classic")
        self.diff_option.set(diff_name)

        self._set_stat(self.max_hp_entry, player.max_hp)
        self._set_stat(self.hp_entry, player.hp)
        self._set_stat(self.max_mana_entry, player.max_mana)
        self._set_stat(self.mana_entry, player.mana)
        self._set_stat(self.hair_style_entry, player.hair_style)

        # Load colors
        for attr_name, (preview_box, hex_entry) in self.color_widgets.items():
            color_obj: Color = getattr(player, attr_name, Color())
            hex_str = color_obj.to_hex()
            hex_entry.delete(0, "end")
            hex_entry.insert(0, hex_str)
            preview_box.configure(fg_color=hex_str)

    def apply_to_player(self) -> Player:
        if not self.player:
            return None
        
        self.player.name = self.name_entry.get().strip() or "Terrarian"
        diff_str = self.diff_option.get()
        self.player.difficulty = GAME_MODE_IDS.get(diff_str, 0)

        try:
            self.player.max_hp = int(self.max_hp_entry.get().strip())
        except ValueError:
            pass

        try:
            self.player.hp = int(self.hp_entry.get().strip())
        except ValueError:
            pass

        try:
            self.player.max_mana = int(self.max_mana_entry.get().strip())
        except ValueError:
            pass

        try:
            self.player.mana = int(self.mana_entry.get().strip())
        except ValueError:
            pass

        try:
            self.player.hair_style = int(self.hair_style_entry.get().strip())
        except ValueError:
            pass

        # Save colors
        for attr_name, (preview_box, hex_entry) in self.color_widgets.items():
            hex_str = hex_entry.get().strip()
            color_obj = Color.from_hex(hex_str)
            setattr(self.player, attr_name, color_obj)

        return self.player
