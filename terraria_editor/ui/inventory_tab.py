import customtkinter as ctk
from ..models import Player, InventoryItem, ITEM_NAMES, PREFIX_NAMES

class InventoryTab(ctk.CTkFrame):
    def __init__(self, parent, on_data_changed_callback):
        super().__init__(parent)
        self.on_data_changed = on_data_changed_callback
        self.player: Player = None
        self.selected_slot_index: int = 0
        self.slot_buttons = []

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self._build_ui()

    def _build_ui(self):
        # Left Panel: Inventory Grid
        grid_card = ctk.CTkFrame(self, corner_radius=10, fg_color="#1E1E2E")
        grid_card.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(grid_card, text="🎒 Inventory Slots (50 Main + Coins & Ammo)", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))

        scroll_grid = ctk.CTkScrollableFrame(grid_card, fg_color="transparent")
        scroll_grid.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Build 5x10 grid of main slots (0..49) plus 2x4 coins/ammo slots (50..57)
        grid_frame = ctk.CTkFrame(scroll_grid, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)

        for i in range(58):
            row = i // 5
            col = i % 5
            
            btn_color = "#313244"
            if i >= 50 and i <= 53:
                # Coins
                btn_color = "#45475A"
            elif i >= 54:
                # Ammo
                btn_color = "#363A4F"

            btn = ctk.CTkButton(
                grid_frame,
                text=f"[{i+1}]\nEmpty",
                font=ctk.CTkFont(size=10),
                width=85,
                height=50,
                corner_radius=6,
                fg_color=btn_color,
                hover_color="#585B70",
                command=lambda idx=i: self._select_slot(idx)
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.slot_buttons.append(btn)

        # Right Panel: Selected Slot Details & Quick Actions
        details_card = ctk.CTkFrame(self, corner_radius=10, fg_color="#1E1E2E")
        details_card.grid(row=0, column=1, padx=(10, 15), pady=15, sticky="nsew")

        ctk.CTkLabel(details_card, text="⚡ Slot Inspector & Editor", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))

        self.slot_title_lbl = ctk.CTkLabel(details_card, text="Selected Slot: #1", font=ctk.CTkFont(size=14, weight="bold"), text_color="#89B4FA")
        self.slot_title_lbl.pack(anchor="w", padx=15, pady=(0, 10))

        # Preset Quick Add Search / Dropdown
        ctk.CTkLabel(details_card, text="Quick Item Presets:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(5, 2))
        item_preset_options = [f"{name} (ID: {item_id})" for item_id, name in ITEM_NAMES.items()]
        self.preset_option = ctk.CTkOptionMenu(details_card, values=item_preset_options, command=self._on_preset_selected)
        self.preset_option.pack(fill="x", padx=15, pady=(0, 15))

        # Item ID Input
        id_f = ctk.CTkFrame(details_card, fg_color="transparent")
        id_f.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(id_f, text="Item ID:", width=80, anchor="w", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        self.item_id_entry = ctk.CTkEntry(id_f)
        self.item_id_entry.pack(side="left", fill="x", expand=True)

        # Stack Size Input
        stack_f = ctk.CTkFrame(details_card, fg_color="transparent")
        stack_f.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(stack_f, text="Stack Size:", width=80, anchor="w", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        self.stack_entry = ctk.CTkEntry(stack_f)
        self.stack_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        max_stack_btn = ctk.CTkButton(stack_f, text="9999", width=50, fg_color="#A6E3A1", text_color="#11111B", command=lambda: self._set_entry(self.stack_entry, 9999))
        max_stack_btn.pack(side="left")

        # Prefix / Modifier Dropdown
        prefix_f = ctk.CTkFrame(details_card, fg_color="transparent")
        prefix_f.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(prefix_f, text="Prefix:", width=80, anchor="w", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        prefix_options = [f"{p_name} ({p_id})" for p_id, p_name in PREFIX_NAMES.items()]
        self.prefix_option = ctk.CTkOptionMenu(prefix_f, values=prefix_options)
        self.prefix_option.pack(side="left", fill="x", expand=True)

        # Apply Changes to Slot Button
        apply_btn = ctk.CTkButton(details_card, text="Apply Changes to Slot", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#FAB387", hover_color="#F9E2AF", text_color="#11111B", height=35, command=self._apply_slot_changes)
        apply_btn.pack(fill="x", padx=15, pady=15)

        # Divider
        ctk.CTkFrame(details_card, height=2, fg_color="#313244").pack(fill="x", padx=15, pady=10)

        # Global Quick Actions
        ctk.CTkLabel(details_card, text="✨ Quick Inventory Presets", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=15, pady=(5, 5))

        clear_btn = ctk.CTkButton(details_card, text="Clear Selected Slot", fg_color="#F38BA8", hover_color="#EBA0AC", text_color="#11111B", command=self._clear_slot)
        clear_btn.pack(fill="x", padx=15, pady=4)

        plat_btn = ctk.CTkButton(details_card, text="Give 9999 Platinum Coins", fg_color="#F9E2AF", hover_color="#FAB387", text_color="#11111B", command=self._give_platinum_coins)
        plat_btn.pack(fill="x", padx=15, pady=4)

        endgame_btn = ctk.CTkButton(details_card, text="Add Endgame Starter Pack (Zenith + Solar)", fg_color="#CBA6F7", hover_color="#B4BEFE", text_color="#11111B", command=self._give_endgame_pack)
        endgame_btn.pack(fill="x", padx=15, pady=4)

    def _set_entry(self, entry_widget, val):
        entry_widget.delete(0, "end")
        entry_widget.insert(0, str(val))

    def _on_preset_selected(self, choice: str):
        # Extract item ID from string choice e.g. "Zenith (ID: 4956)"
        if "ID: " in choice:
            item_id_str = choice.split("ID: ")[1].rstrip(")")
            self._set_entry(self.item_id_entry, item_id_str)
            if not self.stack_entry.get() or self.stack_entry.get() == "0":
                self._set_entry(self.stack_entry, 1)

    def _select_slot(self, slot_idx: int):
        self.selected_slot_index = slot_idx
        self.slot_title_lbl.configure(text=f"Selected Slot: #{slot_idx + 1}")

        if self.player and slot_idx < len(self.player.inventory):
            item = self.player.inventory[slot_idx]
            self._set_entry(self.item_id_entry, item.id)
            self._set_entry(self.stack_entry, item.stack)
            
            p_name = PREFIX_NAMES.get(item.prefix, "None")
            self.prefix_option.set(f"{p_name} ({item.prefix})")

    def _update_grid_display(self):
        if not self.player:
            return
        for i, item in enumerate(self.player.inventory[:58]):
            if i < len(self.slot_buttons):
                if item.id > 0:
                    prefix_str = f"[{PREFIX_NAMES.get(item.prefix, '')[:3]}] " if item.prefix > 0 else ""
                    text = f"[{i+1}]\n{prefix_str}{item.name[:10]}\nx{item.stack}"
                    self.slot_buttons[i].configure(text=text, fg_color="#89B4FA", text_color="#11111B")
                else:
                    btn_color = "#45475A" if (50 <= i <= 53) else ("#363A4F" if i >= 54 else "#313244")
                    self.slot_buttons[i].configure(text=f"[{i+1}]\nEmpty", fg_color=btn_color, text_color="#CDD6F4")

    def load_player_data(self, player: Player):
        self.player = player
        self._update_grid_display()
        self._select_slot(0)

    def apply_to_player(self) -> Player:
        self._apply_slot_changes()
        return self.player

    def _apply_slot_changes(self):
        if not self.player or self.selected_slot_index >= len(self.player.inventory):
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

        self.player.inventory[self.selected_slot_index] = InventoryItem(id=item_id, stack=stack, prefix=prefix_id)
        self._update_grid_display()

    def _clear_slot(self):
        self._set_entry(self.item_id_entry, 0)
        self._set_entry(self.stack_entry, 0)
        self.prefix_option.set("None (0)")
        self._apply_slot_changes()

    def _give_platinum_coins(self):
        if not self.player:
            return
        # Coins slots are 50, 51, 52, 53
        self.player.inventory[50] = InventoryItem(id=74, stack=9999, prefix=0)
        self._update_grid_display()
        self._select_slot(50)

    def _give_endgame_pack(self):
        if not self.player:
            return
        # Add Zenith (4956), Terraprisma (4923), Solar Helmet (3507), Breastplate (3508), Leggings (3509)
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
        self._select_slot(0)
