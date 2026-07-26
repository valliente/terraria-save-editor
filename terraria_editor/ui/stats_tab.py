import customtkinter as ctk
from tkinter import colorchooser
from ..models import Player, GAME_MODES, GAME_MODE_IDS, Color

class StatsTab(ctk.CTkFrame):
    def __init__(self, parent, on_data_changed_callback):
        super().__init__(parent, fg_color="transparent")
        self.on_data_changed = on_data_changed_callback
        self.player: Player = None

        self.accent_color = "#1DB954"
        self.frame_bg = "#1A1A1A"
        self.input_bg = "#222222"

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._build_ui()

    def _build_ui(self):
        # Header
        header_lbl = ctk.CTkLabel(self, text="CHARACTER: None", font=ctk.CTkFont(size=20, weight="bold"), text_color="#FFFFFF", anchor="w")
        header_lbl.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="ew")
        self.header_lbl = header_lbl

        # Main content area
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(1, weight=1)

        # Character Preview Panel (Left)
        preview_frame = ctk.CTkFrame(content_frame, width=220, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        preview_frame.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="ns")
        preview_frame.grid_propagate(False)
        
        # Stylized glowing effect on the character preview panel
        glow_frame = ctk.CTkFrame(preview_frame, corner_radius=8, fg_color="transparent", border_color=self.accent_color, border_width=2)
        glow_frame.pack(expand=True, fill="both", padx=15, pady=15)
        
        ctk.CTkLabel(glow_frame, text="[Character\nPreview]", text_color=self.accent_color, font=ctk.CTkFont(size=16, weight="bold")).pack(expand=True)

        # Right Panel: Inputs
        inputs_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        inputs_frame.grid(row=0, column=1, padx=(10, 20), pady=10, sticky="nsew")
        inputs_frame.grid_columnconfigure((0, 1), weight=1)

        input_kwargs = {
            "fg_color": self.input_bg,
            "border_color": self.accent_color,
            "border_width": 1,
            "text_color": "#FFFFFF",
            "font": ctk.CTkFont(size=14)
        }

        # Player Name
        ctk.CTkLabel(inputs_frame, text="Player Name:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=10, pady=(5, 2), sticky="w")
        self.name_entry = ctk.CTkEntry(inputs_frame, **input_kwargs)
        self.name_entry.grid(row=1, column=0, padx=10, pady=(0, 15), sticky="ew")

        # Game Mode
        ctk.CTkLabel(inputs_frame, text="Game Mode:", font=ctk.CTkFont(size=13)).grid(row=0, column=1, padx=10, pady=(5, 2), sticky="w")
        self.diff_option = ctk.CTkOptionMenu(
            inputs_frame, 
            values=list(GAME_MODE_IDS.keys()),
            fg_color=self.input_bg,
            button_color=self.input_bg,
            button_hover_color="#333333",
            dropdown_fg_color=self.input_bg,
            dropdown_hover_color="#333333",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=14)
        )

        self.diff_option.grid(row=1, column=1, padx=10, pady=(0, 15), sticky="ew")

        # Max HP
        ctk.CTkLabel(inputs_frame, text="Max HP:", font=ctk.CTkFont(size=13)).grid(row=2, column=0, padx=10, pady=(5, 2), sticky="w")
        self.max_hp_entry = ctk.CTkEntry(inputs_frame, **input_kwargs)
        self.max_hp_entry.grid(row=3, column=0, padx=10, pady=(0, 15), sticky="ew")

        # Max Mana
        ctk.CTkLabel(inputs_frame, text="Max Mana:", font=ctk.CTkFont(size=13)).grid(row=2, column=1, padx=10, pady=(5, 2), sticky="w")
        self.max_mana_entry = ctk.CTkEntry(inputs_frame, **input_kwargs)
        self.max_mana_entry.grid(row=3, column=1, padx=10, pady=(0, 15), sticky="ew")

        # Appearance Section
        appearance_lbl = ctk.CTkLabel(inputs_frame, text="Appearance", font=ctk.CTkFont(size=14, weight="bold"))
        appearance_lbl.grid(row=4, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        # Swatches layout
        colors_frame = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        colors_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Hair Style
        hair_f = ctk.CTkFrame(colors_frame, fg_color="transparent")
        hair_f.pack(side="left", padx=(0, 20))
        ctk.CTkLabel(hair_f, text="Hair Style", font=ctk.CTkFont(size=12)).pack(anchor="center")
        self.hair_style_entry = ctk.CTkEntry(hair_f, width=60, justify="center", **input_kwargs)
        self.hair_style_entry.pack(pady=5)

        # Colors
        self.color_widgets = {}
        colors_to_edit = [
            ("Skin", "skin_color"),
            ("Eye", "eye_color"),
            ("Clothes", "shirt_color"),
            ("Armor", "pants_color"),
        ]

        for lbl, attr in colors_to_edit:
            col_f = ctk.CTkFrame(colors_frame, fg_color="transparent")
            col_f.pack(side="left", padx=10)
            ctk.CTkLabel(col_f, text=lbl, font=ctk.CTkFont(size=12)).pack(anchor="center")
            
            # Glowing border around color swatch
            swatch_border = ctk.CTkFrame(col_f, width=32, height=32, corner_radius=6, fg_color="transparent", border_color=self.accent_color, border_width=2)
            swatch_border.pack(pady=5)
            swatch_border.pack_propagate(False)
            
            swatch = ctk.CTkButton(swatch_border, text="", width=24, height=24, corner_radius=4, command=lambda a=attr: self._pick_color(a))
            swatch.pack(expand=True)
            
            self.color_widgets[attr] = swatch

        # Bottom Actions
        actions_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        actions_frame.grid(row=2, column=0, sticky="ew")
        actions_frame.grid_propagate(False)
        
        save_btn = ctk.CTkButton(
            actions_frame, text="Save Changes", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.accent_color, text_color="#121212", 
            hover_color="#158C3E", height=40, width=150,
            command=self._save_changes
        )
        save_btn.pack(side="right", padx=20, pady=10)

    def _save_changes(self):
        self.on_data_changed()
        # Optionally show a "Saved" toast or update the file directly, 
        # but the architecture says `on_data_changed` will sync UI -> player model.

    def _pick_color(self, attr_name: str):
        color_code = colorchooser.askcolor(title=f"Choose {attr_name.replace('_', ' ').title()}")
        if color_code and color_code[1]:
            hex_str = color_code[1]
            self.color_widgets[attr_name].configure(fg_color=hex_str, hover_color=hex_str)
            if self.player:
                setattr(self.player, attr_name, Color.from_hex(hex_str))
                self.on_data_changed()

    def _set_entry(self, entry_widget, value):
        entry_widget.delete(0, "end")
        entry_widget.insert(0, str(value))

    def load_player_data(self, player: Player):
        self.player = player
        self.header_lbl.configure(text=f"CHARACTER: {player.name}")
        self._set_entry(self.name_entry, player.name)

        diff_name = GAME_MODES.get(player.difficulty, "Classic")
        self.diff_option.set(diff_name)

        self._set_entry(self.max_hp_entry, f"{player.hp} / {player.max_hp}")
        self._set_entry(self.max_mana_entry, f"{player.mana} / {player.max_mana}")
        self._set_entry(self.hair_style_entry, player.hair_style)

        # Load colors
        for attr_name, swatch in self.color_widgets.items():
            color_obj: Color = getattr(player, attr_name, Color())
            hex_str = color_obj.to_hex()
            swatch.configure(fg_color=hex_str, hover_color=hex_str)

    def apply_to_player(self) -> Player:
        if not self.player:
            return None
        
        self.player.name = self.name_entry.get().strip() or "Terrarian"
        diff_str = self.diff_option.get()
        self.player.difficulty = GAME_MODE_IDS.get(diff_str, 0)

        # Parse "HP / MaxHP" format
        try:
            hp_str = self.max_hp_entry.get().strip()
            if "/" in hp_str:
                parts = hp_str.split("/")
                self.player.hp = int(parts[0].strip())
                self.player.max_hp = int(parts[1].strip())
            else:
                self.player.hp = int(hp_str)
                self.player.max_hp = int(hp_str)
        except ValueError:
            pass

        try:
            mana_str = self.max_mana_entry.get().strip()
            if "/" in mana_str:
                parts = mana_str.split("/")
                self.player.mana = int(parts[0].strip())
                self.player.max_mana = int(parts[1].strip())
            else:
                self.player.mana = int(mana_str)
                self.player.max_mana = int(mana_str)
        except ValueError:
            pass

        try:
            self.player.hair_style = int(self.hair_style_entry.get().strip())
        except ValueError:
            pass

        return self.player
