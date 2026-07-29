import customtkinter as ctk
from ..models import Player

class JourneyTab(ctk.CTkFrame):
    def __init__(self, parent, on_data_changed_callback):
        super().__init__(parent, fg_color="transparent")
        self.on_data_changed = on_data_changed_callback
        self.player: Player = None

        self.accent_color = "#1DB954"
        self.frame_bg = "#1A1A1A"
        self.input_bg = "#222222"

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build_ui()

    def _build_ui(self):
        # Header
        header_card = ctk.CTkFrame(self, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        header_card.grid(row=0, column=0, columnspan=2, padx=20, pady=(15, 10), sticky="ew")
        
        ctk.CTkLabel(header_card, text="🌟 Journey & Presets Utilities", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.accent_color).pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(header_card, text="Quickly apply endgame presets, manage Journey Mode research, and unlock permanent buffs.", font=ctk.CTkFont(size=12), text_color="#AAAAAA").pack(anchor="w", padx=15, pady=(0, 15))

        # Column 1: Stat Presets & Debuffs
        col1 = ctk.CTkFrame(self, fg_color="transparent")
        col1.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")

        preset_card = ctk.CTkFrame(col1, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        preset_card.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(preset_card, text="Quick Stat Presets", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.accent_color).pack(anchor="w", padx=15, pady=(15, 10))
        
        btn_kwargs = {
            "font": ctk.CTkFont(size=13, weight="bold"),
            "height": 40,
            "fg_color": self.input_bg,
            "border_color": self.accent_color,
            "border_width": 1,
            "hover_color": "#333333",
            "text_color": "#FFFFFF",
        }

        ctk.CTkButton(preset_card, text="❤️ Max HP & Mana (500/200)", command=self._set_max_stats, **btn_kwargs).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(preset_card, text="✨ Purify (Clear Debuffs)", command=self._clear_debuffs, **btn_kwargs).pack(fill="x", padx=15, pady=(5, 15))

        # Journey Mode Card
        journey_card = ctk.CTkFrame(col1, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        journey_card.pack(fill="both", expand=True)

        ctk.CTkLabel(journey_card, text="Journey Mode Research", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.accent_color).pack(anchor="w", padx=15, pady=(15, 10))
        ctk.CTkLabel(journey_card, text="Research unlocking requires the upcoming\nTerraria 1.4.4 API Integration plugin.", text_color="#777777", justify="left").pack(anchor="w", padx=15, pady=5)
        
        ctk.CTkButton(journey_card, text="Unlock All Items (1.4.4+)", state="disabled", fg_color="#111111", text_color="#555555").pack(fill="x", padx=15, pady=10)
        ctk.CTkButton(journey_card, text="Max All Research", command=self._max_research, **btn_kwargs).pack(fill="x", padx=15, pady=(5, 10))

        # Column 2: 1.4.4 Permanent Buffs
        col2 = ctk.CTkFrame(self, fg_color="transparent")
        col2.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="nsew")

        buff_card = ctk.CTkFrame(col2, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        buff_card.pack(fill="both", expand=True)

        ctk.CTkLabel(buff_card, text="1.4.4 Permanent Buffs", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.accent_color).pack(anchor="w", padx=15, pady=(15, 10))
        ctk.CTkLabel(buff_card, text="Toggle Shimmer and permanent consumable buffs.", text_color="#AAAAAA").pack(anchor="w", padx=15, pady=(0, 10))

        self.buff_vars = {}
        buffs = [
            ("Aegis Fruit (+Defense)", "aegis_fruit"),
            ("Ambrosia (+Mining/Building Speed)", "ambrosia"),
            ("Arcane Crystal (+Mana Regen)", "arcane_crystal"),
            ("Galaxy Pearl (+Luck)", "galaxy_pearl"),
            ("Gummy Worm (+Fishing Skill)", "gummy_worm"),
            ("Peddler's Satchel (+Travelling Merchant)", "peddlers_satchel"),
            ("Demon Heart (+Accessory Slot)", "demon_heart"),
            ("Minecart Upgrade", "minecart_upgrade")
        ]

        for text, key in buffs:
            var = ctk.BooleanVar(value=False)
            self.buff_vars[key] = var
            cb = ctk.CTkCheckBox(buff_card, text=text, variable=var, fg_color=self.accent_color, hover_color="#158C3E", border_color="#555555")
            cb.pack(anchor="w", padx=15, pady=8)

        ctk.CTkLabel(buff_card, text="Note: Checkboxes are visual placeholders until the\nbinary serialization for 1.4.4 is finalized.", text_color="#666666", font=ctk.CTkFont(size=10)).pack(anchor="w", padx=15, pady=(15, 5))
        
        ctk.CTkButton(buff_card, text="Unlock All 1.4.4 & 1.4.5 Buffs", command=self._unlock_all_buffs, fg_color=self.input_bg, border_color=self.accent_color, border_width=1, hover_color="#333333", text_color="#FFFFFF", height=35).pack(fill="x", padx=15, pady=10)

    def load_player_data(self, player: Player):
        self.player = player

    def apply_to_player(self) -> Player:
        # Binary serialization for buffs is skipped to prevent corruption in v2.101
        return self.player

    def _set_max_stats(self):
        if not self.player: return
        self.player.hp = 500
        self.player.max_hp = 500
        self.player.mana = 200
        self.player.max_mana = 200
        self.on_data_changed()

    def _clear_debuffs(self):
        if not self.player: return
        pass

    def _max_research(self):
        if not self.player: return
        pass

    def _unlock_all_buffs(self):
        if not self.player: return
        for var in self.buff_vars.values():
            var.set(True)
