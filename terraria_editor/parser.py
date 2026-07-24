import io
import os
import shutil
import struct
from typing import Tuple
from .models import Player, Color, InventoryItem
from .crypto import decrypt_plr, encrypt_plr, KEY_68332866

class BinaryReader:
    def __init__(self, data: bytes):
        self.stream = io.BytesIO(data)

    def read_byte(self) -> int:
        b = self.stream.read(1)
        if not b:
            return 0
        return b[0]

    def read_bool(self) -> bool:
        return self.read_byte() != 0

    def read_int16(self) -> int:
        data = self.stream.read(2)
        if len(data) < 2:
            return 0
        return struct.unpack("<h", data)[0]

    def read_int32(self) -> int:
        data = self.stream.read(4)
        if len(data) < 4:
            return 0
        return struct.unpack("<i", data)[0]

    def read_int64(self) -> int:
        data = self.stream.read(8)
        if len(data) < 8:
            return 0
        return struct.unpack("<q", data)[0]

    def read_7bit_encoded_int(self) -> int:
        result = 0
        shift = 0
        while True:
            b = self.read_byte()
            result |= (b & 0x7F) << shift
            if (b & 0x80) == 0:
                break
            shift += 7
        return result

    def read_string(self) -> str:
        length = self.read_7bit_encoded_int()
        data = self.stream.read(length)
        return data.decode("utf-8", errors="ignore")

    def read_color(self) -> Color:
        r = self.read_byte()
        g = self.read_byte()
        b = self.read_byte()
        return Color(r, g, b)

    def read_item(self) -> InventoryItem:
        item_id = self.read_int32()
        stack = self.read_int32()
        prefix = self.read_byte()
        favorite = self.read_bool()
        return InventoryItem(id=item_id, stack=stack, prefix=prefix, favorite=favorite)

    def remaining_bytes(self) -> bytes:
        return self.stream.read()

    @property
    def position(self) -> int:
        return self.stream.tell()

class BinaryWriter:
    def __init__(self):
        self.stream = io.BytesIO()

    def write_byte(self, value: int):
        self.stream.write(bytes([value & 0xFF]))

    def write_bool(self, value: bool):
        self.write_byte(1 if value else 0)

    def write_int16(self, value: int):
        self.stream.write(struct.pack("<h", value))

    def write_int32(self, value: int):
        self.stream.write(struct.pack("<i", value))

    def write_int64(self, value: int):
        self.stream.write(struct.pack("<q", value))

    def write_7bit_encoded_int(self, value: int):
        v = value & 0xFFFFFFFF
        while v >= 0x80:
            self.stream.write(bytes([(v & 0x7F) | 0x80]))
            v >>= 7
        self.stream.write(bytes([v & 0x7F]))

    def write_string(self, text: str):
        encoded = text.encode("utf-8")
        self.write_7bit_encoded_int(len(encoded))
        self.stream.write(encoded)

    def write_color(self, color: Color):
        self.write_byte(color.r)
        self.write_byte(color.g)
        self.write_byte(color.b)

    def write_item(self, item: InventoryItem):
        self.write_int32(item.id)
        self.write_int32(item.stack)
        self.write_byte(item.prefix)
        self.write_bool(item.favorite)

    def write_bytes(self, data: bytes):
        self.stream.write(data)

    def get_bytes(self) -> bytes:
        return self.stream.getvalue()


class PLRFileHandler:
    def __init__(self):
        self.current_file_path: str = ""
        self.key_used: bytes = KEY_68332866
        self.raw_trailing_data: bytes = b""
        self.player: Player = Player()

    def load_plr(self, file_path: str) -> Player:
        """
        Loads and decrypts a Terraria .plr file, returning a Player model.
        """
        with open(file_path, "rb") as f:
            raw_encrypted = f.read()

        decrypted, key_used = decrypt_plr(raw_encrypted)
        self.current_file_path = file_path
        self.key_used = key_used

        reader = BinaryReader(decrypted)
        
        # Read header
        version = reader.read_int32()
        magic = reader.read_string() # "relogic"
        file_type = reader.read_byte()
        revision = reader.read_int32()
        favorite = reader.read_int64()

        # Read player metadata
        name = reader.read_string()
        difficulty = reader.read_byte()
        play_time_ticks = reader.read_int64()
        hair_style = reader.read_int32()
        hair_dye = reader.read_byte()
        hide_visuals = reader.read_byte()
        hide_visuals2 = reader.read_byte()
        hide_misc = reader.read_byte()
        skin_variant = reader.read_byte()

        # Stats
        hp = reader.read_int32()
        max_hp = reader.read_int32()
        mana = reader.read_int32()
        max_mana = reader.read_int32()
        extra_accessory = reader.read_bool()
        downed_dd2 = reader.read_bool()
        tax_collector = reader.read_bool()

        # Colors
        hair_color = reader.read_color()
        skin_color = reader.read_color()
        eye_color = reader.read_color()
        shirt_color = reader.read_color()
        undershirt_color = reader.read_color()
        pants_color = reader.read_color()
        shoe_color = reader.read_color()

        # Items
        inventory = [reader.read_item() for _ in range(58)]
        armor = [reader.read_item() for _ in range(20)]
        dye = [reader.read_item() for _ in range(10)]
        misc_eq = [reader.read_item() for _ in range(5)]

        # Store trailing data to preserve additional banks / modded info without corruption
        self.raw_trailing_data = reader.remaining_bytes()

        self.player = Player(
            version=version,
            file_type=magic,
            name=name,
            difficulty=difficulty,
            play_time_ticks=play_time_ticks,
            hair_style=hair_style,
            hair_dye=hair_dye,
            hide_visuals=hide_visuals,
            hide_visuals2=hide_visuals2,
            hide_misc=hide_misc,
            skin_variant=skin_variant,
            hp=hp,
            max_hp=max_hp,
            mana=mana,
            max_mana=max_mana,
            extra_accessory=extra_accessory,
            downed_dd2_event=downed_dd2,
            tax_collector_paid=tax_collector,
            hair_color=hair_color,
            skin_color=skin_color,
            eye_color=eye_color,
            shirt_color=shirt_color,
            undershirt_color=undershirt_color,
            pants_color=pants_color,
            shoe_color=shoe_color,
            inventory=inventory,
            armor=armor,
            dye=dye,
            misc_eq=misc_eq
        )
        return self.player

    def save_plr(self, target_path: str = None) -> str:
        """
        Saves changes to target_path (or self.current_file_path).
        Automatically creates a .plr.bak backup before writing.
        Returns path to the backup file created.
        """
        file_path = target_path or self.current_file_path
        if not file_path:
            raise ValueError("No target file path specified for saving.")

        # Step 1: Auto-backup
        backup_path = file_path + ".bak"
        if os.path.exists(file_path):
            shutil.copy2(file_path, backup_path)

        # Step 2: Build unencrypted binary data
        writer = BinaryWriter()
        p = self.player

        writer.write_int32(p.version if p.version > 0 else 230)
        writer.write_string("relogic")
        writer.write_byte(2) # Player file type
        writer.write_int32(1) # revision
        writer.write_int64(0) # favorite bitmask

        writer.write_string(p.name)
        writer.write_byte(p.difficulty)
        writer.write_int64(p.play_time_ticks)
        writer.write_int32(p.hair_style)
        writer.write_byte(p.hair_dye)
        writer.write_byte(p.hide_visuals)
        writer.write_byte(p.hide_visuals2)
        writer.write_byte(p.hide_misc)
        writer.write_byte(p.skin_variant)

        writer.write_int32(p.hp)
        writer.write_int32(p.max_hp)
        writer.write_int32(p.mana)
        writer.write_int32(p.max_mana)
        writer.write_bool(p.extra_accessory)
        writer.write_bool(p.downed_dd2_event)
        writer.write_bool(p.tax_collector_paid)

        writer.write_color(p.hair_color)
        writer.write_color(p.skin_color)
        writer.write_color(p.eye_color)
        writer.write_color(p.shirt_color)
        writer.write_color(p.undershirt_color)
        writer.write_color(p.pants_color)
        writer.write_color(p.shoe_color)

        for item in p.inventory:
            writer.write_item(item)
        for item in p.armor:
            writer.write_item(item)
        for item in p.dye:
            writer.write_item(item)
        for item in p.misc_eq:
            writer.write_item(item)

        # Write trailing data
        if self.raw_trailing_data:
            writer.write_bytes(self.raw_trailing_data)

        raw_unencrypted = writer.get_bytes()

        # Step 3: Encrypt and write out
        encrypted = encrypt_plr(raw_unencrypted, self.key_used)
        with open(file_path, "wb") as f:
            f.write(encrypted)

        self.current_file_path = file_path
        return backup_path

    def restore_backup(self, backup_path: str = None) -> Player:
        """
        Restores from a .plr.bak file.
        """
        b_path = backup_path or (self.current_file_path + ".bak")
        if not os.path.exists(b_path):
            raise FileNotFoundError(f"Backup file not found at: {b_path}")
        
        target = self.current_file_path or b_path.replace(".bak", "")
        shutil.copy2(b_path, target)
        return self.load_plr(target)
