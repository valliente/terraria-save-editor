import customtkinter as ctk
from ..models import World

class WorldTab(ctk.CTkFrame):
    def __init__(self, parent, on_data_changed_callback):
        super().__init__(parent, fg_color="transparent")
        self.on_data_changed = on_data_changed_callback
        self.world: World = None

        self.accent_color = "#1DB954"
        self.frame_bg = "#1A1A1A"
        self.input_bg = "#222222"

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self._build_ui()

    def _build_ui(self):
        # Left Panel: World Attributes
        left_card = ctk.CTkFrame(self, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        left_card.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="nsew")
        
        ctk.CTkLabel(left_card, text="🌍 World Attributes", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.accent_color).pack(anchor="w", padx=15, pady=(15, 10))

        input_kwargs = {
            "fg_color": self.input_bg,
            "border_color": self.accent_color,
            "border_width": 1,
            "text_color": "#FFFFFF",
        }

        # Name
        f_name = ctk.CTkFrame(left_card, fg_color="transparent")
        f_name.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(f_name, text="World Name:", width=100, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        self.name_entry = ctk.CTkEntry(f_name, **input_kwargs)
        self.name_entry.pack(side="left", fill="x", expand=True)

        # Seed
        f_seed = ctk.CTkFrame(left_card, fg_color="transparent")
        f_seed.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(f_seed, text="Seed:", width=100, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        self.seed_entry = ctk.CTkEntry(f_seed, **input_kwargs)
        self.seed_entry.pack(side="left", fill="x", expand=True)

        # Dropdowns
        self.size_var = ctk.StringVar(value="Small")
        self.diff_var = ctk.StringVar(value="Classic")
        self.evil_var = ctk.StringVar(value="Corrupt")
        
        for lbl, var, opts in [
            ("Size:", self.size_var, ["Small", "Medium", "Large"]),
            ("Difficulty:", self.diff_var, ["Journey", "Classic", "Expert", "Master"]),
            ("World Evil:", self.evil_var, ["Corrupt", "Crimson"])
        ]:
            f = ctk.CTkFrame(left_card, fg_color="transparent")
            f.pack(fill="x", padx=15, pady=5)
            ctk.CTkLabel(f, text=lbl, width=100, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
            opt = ctk.CTkOptionMenu(f, variable=var, values=opts, fg_color=self.input_bg, button_color=self.input_bg, dropdown_fg_color=self.input_bg)
            opt.pack(side="left", fill="x", expand=True)

        # Right Panel: Flags
        right_card = ctk.CTkScrollableFrame(self, corner_radius=10, fg_color=self.frame_bg, border_color="#333333", border_width=1)
        right_card.grid(row=0, column=1, padx=(10, 15), pady=15, sticky="nsew")

        ctk.CTkLabel(right_card, text="🚩 World Flags & Bosses", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.accent_color).pack(anchor="w", padx=15, pady=(15, 10))

        self.hardmode_var = ctk.BooleanVar()
        ctk.CTkSwitch(right_card, text="Hardmode Enabled", variable=self.hardmode_var, progress_color=self.accent_color, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=5)
        
        ctk.CTkFrame(right_card, height=1, fg_color="#333333").pack(fill="x", padx=15, pady=10)

        # Bosses
        self.boss_vars = {}
        bosses = [
            ("downed_slime_king", "King Slime"), ("downed_eye_of_cthulhu", "Eye of Cthulhu"), 
            ("downed_eater_brain", "Eater of Worlds / Brain of Cthulhu"), ("downed_skeletron", "Skeletron"),
            ("downed_wall_of_flesh", "Wall of Flesh"), ("downed_mech_boss_1", "The Twins"),
            ("downed_mech_boss_2", "The Destroyer"), ("downed_mech_boss_3", "Skeletron Prime"),
            ("downed_plantera", "Plantera"), ("downed_golem", "Golem"),
            ("downed_duke_fishron", "Duke Fishron"), ("downed_empress", "Empress of Light"),
            ("downed_cultist", "Lunatic Cultist"), ("downed_moon_lord", "Moon Lord")
        ]
        
        for attr, label in bosses:
            var = ctk.BooleanVar()
            self.boss_vars[attr] = var
            ctk.CTkSwitch(right_card, text=label, variable=var, progress_color=self.accent_color).pack(anchor="w", padx=15, pady=2)

        ctk.CTkFrame(right_card, height=1, fg_color="#333333").pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(right_card, text="🏠 NPC Housing (Coming Soon)", font=ctk.CTkFont(size=14, weight="bold"), text_color=self.accent_color).pack(anchor="w", padx=15, pady=(5, 5))
        ctk.CTkLabel(right_card, text="NPC unlocking requires deeper binary pointer shifts.", font=ctk.CTkFont(size=11, slant="italic"), text_color="#666666").pack(anchor="w", padx=15)

    def load_world_data(self, world: World):
        self.world = world
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, world.name)
        self.seed_entry.delete(0, "end")
        self.seed_entry.insert(0, world.seed)
        
        self.size_var.set(world.size)
        self.diff_var.set(world.difficulty)
        self.evil_var.set(world.world_evil)
        
        self.hardmode_var.set(world.hardmode)
        
        for attr, var in self.boss_vars.items():
            var.set(getattr(world, attr, False))

    def apply_to_world(self) -> World:
        if not self.world:
            return None
            
        self.world.name = self.name_entry.get().strip() or "World"
        self.world.seed = self.seed_entry.get().strip() or "RandomSeed"
        self.world.size = self.size_var.get()
        self.world.difficulty = self.diff_var.get()
        self.world.world_evil = self.evil_var.get()
        self.world.hardmode = self.hardmode_var.get()
        
        for attr, var in self.boss_vars.items():
            setattr(self.world, attr, var.get())
            
        return self.world
