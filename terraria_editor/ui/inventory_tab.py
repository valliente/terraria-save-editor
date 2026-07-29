import customtkinter as ctk
from ..models import Player, InventoryItem, ITEM_NAMES, PREFIX_NAMES

class InventoryTab(ctk.CTkFrame):
    def __init__(self, parent, on_data_changed_callback):
        super().__init__(parent, fg_color="transparent")
        self.on_data_changed = on_data_changed_callback
        self.player: Player = None
        self.selected_slot_index: int = 0
        self.selected_slot_array: str = "inventory" # "inventory", "armor", "dye", "misc_eq"
        self.slot_buttons = {} # (array_name, idx): btn

        self.accent_color = "#1DB954"
        self.frame_bg = "#1A1A1A"
        self.input_bg = "#222222"

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self._build_ui()

    def _build_ui(self):
        # Left Panel: Inventory Grid
        grid_card = ctk.CTkFrame(self, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        grid_card.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="nsew")
        grid_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(grid_card, text="🎒 Interactive Inventory Grid", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.accent_color).pack(anchor="w", padx=15, pady=(15, 10))

        scroll_grid = ctk.CTkScrollableFrame(grid_card, fg_color="transparent")
        scroll_grid.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Hotbar (0-9)
        self._create_section(scroll_grid, "Hotbar", "inventory", 0, 10, cols=10)
        # Main (10-49)
        self._create_section(scroll_grid, "Main Inventory", "inventory", 10, 50, cols=10)
        # Coins & Ammo (50-57)
        self._create_section(scroll_grid, "Coins & Ammo", "inventory", 50, 58, cols=4)
        
        # Armor/Accessories (20 slots)
        self._create_section(scroll_grid, "Armor & Accessories", "armor", 0, 20, cols=5)
        # Dyes (10 slots)
        self._create_section(scroll_grid, "Vanity & Dyes", "dye", 0, 10, cols=5)
        # Misc (5 slots)
        self._create_section(scroll_grid, "Misc Equipment", "misc_eq", 0, 5, cols=5)
        
        # Banks (Coming soon)
        ctk.CTkLabel(scroll_grid, text="Storage Banks", font=ctk.CTkFont(size=13, weight="bold"), text_color="#AAAAAA").pack(anchor="w", pady=(10, 5))
        ctk.CTkLabel(scroll_grid, text="(Piggy Bank, Safe, Void Vault editing coming soon pending 1.4.4 API updates)", font=ctk.CTkFont(size=11, slant="italic"), text_color="#666666").pack(anchor="w")

        # Right Panel: Selected Slot Details & Quick Actions
        details_card = ctk.CTkFrame(self, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        details_card.grid(row=0, column=1, padx=(10, 15), pady=15, sticky="nsew")

        ctk.CTkLabel(details_card, text="⚡ Slot Editor", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.accent_color).pack(anchor="w", padx=15, pady=(15, 10))

        self.slot_title_lbl = ctk.CTkLabel(details_card, text="Selected Slot: Hotbar #1", font=ctk.CTkFont(size=14, weight="bold"), text_color="#FFFFFF")
        self.slot_title_lbl.pack(anchor="w", padx=15, pady=(0, 10))

        input_kwargs = {
            "fg_color": self.input_bg,
            "border_color": self.accent_color,
            "border_width": 1,
            "text_color": "#FFFFFF",
        }

        # Preset Quick Add Search / Dropdown
        ctk.CTkLabel(details_card, text="Live Search Items:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(5, 2))
        
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self._filter_presets)
        
        search_entry = ctk.CTkEntry(details_card, textvariable=self.search_var, placeholder_text="Type to search...", **input_kwargs)
        search_entry.pack(fill="x", padx=15, pady=(0, 5))
        
        self.item_preset_options = [f"{name} (ID: {item_id})" for item_id, name in ITEM_NAMES.items()]
        self.preset_option = ctk.CTkOptionMenu(
            details_card, 
            values=self.item_preset_options, 
            command=self._on_preset_selected,
            fg_color=self.input_bg,
            button_color=self.input_bg,
            button_hover_color="#333333",
            dropdown_fg_color=self.input_bg,
            text_color="#FFFFFF",
        )
        self.preset_option.pack(fill="x", padx=15, pady=(0, 15))

        # Item ID Input
        id_f = ctk.CTkFrame(details_card, fg_color="transparent")
        id_f.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(id_f, text="Item ID:", width=80, anchor="w", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        self.item_id_entry = ctk.CTkEntry(id_f, **input_kwargs)
        self.item_id_entry.pack(side="left", fill="x", expand=True)

        # Stack Size Input
        stack_f = ctk.CTkFrame(details_card, fg_color="transparent")
        stack_f.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(stack_f, text="Stack Size:", width=80, anchor="w", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        self.stack_entry = ctk.CTkEntry(stack_f, width=50, **input_kwargs)
        self.stack_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkButton(stack_f, text="99", width=30, fg_color=self.input_bg, border_color=self.accent_color, border_width=1, hover_color="#333333", text_color="#FFFFFF", command=lambda: self._set_entry(self.stack_entry, 99)).pack(side="left", padx=1)
        ctk.CTkButton(stack_f, text="999", width=35, fg_color=self.input_bg, border_color=self.accent_color, border_width=1, hover_color="#333333", text_color="#FFFFFF", command=lambda: self._set_entry(self.stack_entry, 999)).pack(side="left", padx=1)
        ctk.CTkButton(stack_f, text="9999", width=40, fg_color=self.input_bg, border_color=self.accent_color, border_width=1, hover_color="#333333", text_color="#FFFFFF", command=lambda: self._set_entry(self.stack_entry, 9999)).pack(side="left", padx=1)

        # Prefix / Modifier Dropdown
        prefix_f = ctk.CTkFrame(details_card, fg_color="transparent")
        prefix_f.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(prefix_f, text="Prefix:", width=80, anchor="w", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        prefix_options = [f"{p_name} ({p_id})" for p_id, p_name in PREFIX_NAMES.items()]
        self.prefix_option = ctk.CTkOptionMenu(
            prefix_f, 
            values=prefix_options,
            fg_color=self.input_bg,
            button_color=self.input_bg,
            button_hover_color="#333333",
            dropdown_fg_color=self.input_bg,
            text_color="#FFFFFF",
        )
        self.prefix_option.pack(side="left", fill="x", expand=True)

        # Apply Changes to Slot Button
        apply_btn = ctk.CTkButton(
            details_card, text="Apply Changes to Slot", 
            font=ctk.CTkFont(size=13, weight="bold"), 
            fg_color=self.accent_color, 
            text_color="#121212", 
            hover_color="#158C3E", 
            height=35, 
            command=self._apply_slot_changes
        )
        apply_btn.pack(fill="x", padx=15, pady=15)

        # Divider
        ctk.CTkFrame(details_card, height=1, fg_color="#333333").pack(fill="x", padx=15, pady=10)

        # Global Quick Actions
        ctk.CTkLabel(details_card, text="✨ Quick Inventory Presets", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.accent_color).pack(anchor="w", padx=15, pady=(5, 5))

        btn_kwargs = {
            "fg_color": self.input_bg,
            "border_color": self.accent_color,
            "border_width": 1,
            "hover_color": "#333333",
            "text_color": "#FFFFFF",
        }

        clear_btn = ctk.CTkButton(details_card, text="Clear Selected Slot", command=self._clear_slot, **btn_kwargs)
        clear_btn.pack(fill="x", padx=15, pady=4)

        plat_btn = ctk.CTkButton(details_card, text="Give 9999 Platinum Coins", command=self._give_platinum_coins, **btn_kwargs)
        plat_btn.pack(fill="x", padx=15, pady=4)

        endgame_btn = ctk.CTkButton(details_card, text="Add Endgame Starter Pack", command=self._give_endgame_pack, **btn_kwargs)
        endgame_btn.pack(fill="x", padx=15, pady=4)

    def _create_section(self, parent, title, array_name, start_idx, end_idx, cols):
        ctk.CTkLabel(parent, text=title, font=ctk.CTkFont(size=13, weight="bold"), text_color="#AAAAAA").pack(anchor="w", pady=(10, 5))
        grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
        grid_frame.pack(fill="x")
        
        count = end_idx - start_idx
        for i in range(count):
            real_idx = start_idx + i
            row = i // cols
            col = i % cols
            
            btn = ctk.CTkButton(
                grid_frame,
                text=f"[{real_idx+1}]\nEmpty",
                font=ctk.CTkFont(size=10),
                width=80 if cols > 5 else 100,
                height=45,
                corner_radius=6,
                fg_color="#222222",
                border_color="#333333",
                border_width=1,
                hover_color="#333333",
                command=lambda an=array_name, ri=real_idx, t=title: self._select_slot(an, ri, t)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.slot_buttons[(array_name, real_idx)] = btn

    def _filter_presets(self, *args):
        search_term = self.search_var.get().lower()
        if not search_term:
            self.preset_option.configure(values=self.item_preset_options[:50])
            self.preset_option.set(self.item_preset_options[0])
        else:
            filtered = []
            for opt in self.item_preset_options:
                if search_term in opt.lower():
                    filtered.append(opt)
                    if len(filtered) >= 50:
                        break
            if filtered:
                self.preset_option.configure(values=filtered)
                self.preset_option.set(filtered[0])
            else:
                self.preset_option.configure(values=["No items found"])
                self.preset_option.set("No items found")

    def _set_entry(self, entry_widget, val):
        entry_widget.delete(0, "end")
        entry_widget.insert(0, str(val))

    def _on_preset_selected(self, choice: str):
        if "ID: " in choice:
            item_id_str = choice.split("ID: ")[1].rstrip(")")
            self._set_entry(self.item_id_entry, item_id_str)
            if not self.stack_entry.get() or self.stack_entry.get() == "0":
                self._set_entry(self.stack_entry, 1)

    def _select_slot(self, array_name: str, slot_idx: int, title: str):
        # Reset border for all buttons
        for btn in self.slot_buttons.values():
            btn.configure(border_color="#333333", border_width=1)
        
        self.selected_slot_array = array_name
        self.selected_slot_index = slot_idx
        self.slot_title_lbl.configure(text=f"Selected: {title} #{slot_idx + 1}")
        
        # Highlight selected button
        if (array_name, slot_idx) in self.slot_buttons:
            self.slot_buttons[(array_name, slot_idx)].configure(border_color=self.accent_color, border_width=2)

        if self.player:
            arr = getattr(self.player, array_name)
            if slot_idx < len(arr):
                item = arr[slot_idx]
                self._set_entry(self.item_id_entry, item.id)
                self._set_entry(self.stack_entry, item.stack)
                p_name = PREFIX_NAMES.get(item.prefix, "None")
                self.prefix_option.set(f"{p_name} ({item.prefix})")

    def _update_single_slot_display(self, array_name: str, idx: int):
        if not self.player: return
        btn = self.slot_buttons.get((array_name, idx))
        if not btn: return
        
        arr = getattr(self.player, array_name)
        if idx < len(arr):
            item = arr[idx]
            if item.id > 0:
                prefix_str = f"[{PREFIX_NAMES.get(item.prefix, '')[:3]}] " if item.prefix > 0 else ""
                text = f"[{idx+1}]\n{prefix_str}{item.name[:10]}\nx{item.stack}"
                btn.configure(text=text, fg_color="#2A2A2A", text_color=self.accent_color)
            else:
                btn.configure(text=f"[{idx+1}]\nEmpty", fg_color="#222222", text_color="#777777")

    def _update_grid_display(self):
        if not self.player:
            return
            
        for (array_name, idx) in self.slot_buttons.keys():
            self._update_single_slot_display(array_name, idx)
                    
        self._select_slot(self.selected_slot_array, self.selected_slot_index, "Slot")

    def load_player_data(self, player: Player):
        self.player = player
        self._update_grid_display()
        self._select_slot("inventory", 0, "Hotbar")

    def apply_to_player(self) -> Player:
        self._apply_slot_changes()
        return self.player

    def _apply_slot_changes(self):
        if not self.player:
            return
            
        arr = getattr(self.player, self.selected_slot_array)
        if self.selected_slot_index >= len(arr):
            return

        try:
            item_id = int(self.item_id_entry.get().strip())
        except ValueError:
            item_id = 0

        try:
            stack = int(self.stack_entry.get().strip())
        except ValueError:
            stack = 1 if item_id > 0 else 0

        prefix_str = self.prefix_option.get()
        try:
            prefix_id = int(prefix_str.split("(")[1].rstrip(")"))
        except Exception:
            prefix_id = 0

        arr[self.selected_slot_index] = InventoryItem(id=item_id, stack=stack, prefix=prefix_id)
        self._update_single_slot_display(self.selected_slot_array, self.selected_slot_index)

    def _clear_slot(self):
        self._set_entry(self.item_id_entry, 0)
        self._set_entry(self.stack_entry, 0)
        self.prefix_option.set("None (0)")
        self._apply_slot_changes()

    def _give_platinum_coins(self):
        if not self.player:
            return
        self.player.inventory[50] = InventoryItem(id=74, stack=9999, prefix=0)
        self._update_grid_display()
        self._select_slot("inventory", 50, "Coins & Ammo")

    def _give_endgame_pack(self):
        if not self.player:
            return
        items = [
            InventoryItem(id=4956, stack=1, prefix=81), # Legendary Zenith
            InventoryItem(id=4923, stack=1, prefix=83), # Mythical Terraprisma
            InventoryItem(id=3507, stack=1, prefix=0),  # Solar Helmet
            InventoryItem(id=3508, stack=1, prefix=0),  # Solar Breastplate
            InventoryItem(id=3509, stack=1, prefix=0),  # Solar Leggings
            InventoryItem(id=3110, stack=1, prefix=65), # Warding Terraspark Boots
            InventoryItem(id=5010, stack=1, prefix=0),  # Rod of Harmony
        ]
        for idx, item in enumerate(items):
            if idx < len(self.player.inventory):
                self.player.inventory[idx] = item
        self._update_grid_display()
        self._select_slot("inventory", 0, "Hotbar")
