import sys

class DolbyVisionVSVDB:
    """
    Manages a 7-byte Dolby Vision Vendor Specific Video Data Block (VSVDB) payload.
    """

    # Lookup tables based on the provided text and common knowledge
    DM_VERSIONS = {
        0b000: "2.9 (e.g., Profile 5)", # Hypothetical, often 2.x is less specific
        0b001: "3.x",
        0b010: "4.x",
        # Add more if known
    }
    DM_VERSIONS_REV = {v: k for k, v in DM_VERSIONS.items()}

    BACKLIGHT_CTRL_MAP = {
        0: "Not Supported",
        1: "Supported"
    }
    BACKLIGHT_CTRL_MAP_REV = {v: k for k, v in BACKLIGHT_CTRL_MAP.items()}

    YUV_SUPPORT_MAP = {
        0: "Not Supported",
        1: "Supported"
    }
    YUV_SUPPORT_MAP_REV = {v: k for k, v in YUV_SUPPORT_MAP.items()}


    # Min Lum Nits (index to value, value is nits string)
    # Based on "MinL nits" and "MinL (dec)" from the user's text
    MIN_LUM_NITS_TABLE = {
        0: 0.0, 1: 0.001, 2: 0.002, 3: 0.005, 4: 0.008, 5: 0.013,
        6: 0.019, 7: 0.026, 8: 0.035, 9: 0.046, 10: 0.058, 11: 0.072,
        12: 0.088, 13: 0.106, 14: 0.127, 15: 0.15, 16: 0.176, 17: 0.204,
        18: 0.236, 19: 0.271, 20: 0.31, 21: 0.353, 22: 0.399, 23: 0.45,
        24: 0.506, 25: 0.566, 26: 0.631, 27: 0.702, 28: 0.779, 29: 0.862,
        30: 0.951, 31: 1.048
    }
    MIN_LUM_NITS_TABLE_REV = {v: k for k, v in MIN_LUM_NITS_TABLE.items()}

    GLOBAL_DIMMING_MAP = {
        0: "Not Supported",
        1: "Supported"
    }
    GLOBAL_DIMMING_MAP_REV = {v: k for k, v in GLOBAL_DIMMING_MAP.items()}

    BACKLIGHT_MIN_LUM_MAP = { # index to nits string
        0b00: "25 nits",
        0b01: "50 nits",
        0b10: "75 nits",
        0b11: "100 nits / Disabled" # Context dependent, using 100 nits as per player led example
    }
    BACKLIGHT_MIN_LUM_MAP_REV = {v: k for k, v in BACKLIGHT_MIN_LUM_MAP.items()}
    # Simplified for setting, prefer "100 nits"
    BACKLIGHT_MIN_LUM_MAP_REV_SET = {
        "25 nits": 0b00, "50 nits": 0b01, "75 nits": 0b10, "100 nits": 0b11, "Disabled": 0b11
    }


    # Max Lum Nits (index to value, value is nits string)
    # Based on "MaxL nits" and "MaxL (dec)" from the user's text
    MAX_LUM_NITS_TABLE = {
        0: 97, 1: 114, 2: 133, 3: 155, 4: 181, 5: 211, 6: 246, 7: 286,
        8: 332, 9: 386, 10: 447, 11: 519, 12: 601, 13: 697, 14: 807,
        15: 935, 16: 1082, 17: 1253, 18: 1450, 19: 1679, 20: 1944,
        21: 2251, 22: 2607, 23: 3021, 24: 3501, 25: 4060, 26: 4710,
        27: 5468, 28: 6351, 29: 7383, 30: 8589, 31: 10000
    }
    MAX_LUM_NITS_TABLE_REV = {v: k for k, v in MAX_LUM_NITS_TABLE.items()}

    DV_MODES = { # Based on byte 3, last 2 bits (bits 0 and 1) of the "Original" payload example
        0b00: "LLDV",
        0b01: "LLDV + LLDV-HDMI", # This enables the "LLDV-HDMI" or "Interface" bit (bit 0 of Reserved/DV Mode)
        0b10: "Std + LLDV",
        0b11: "Std + LLDV + LLDV-HDMI"
    }
    DV_MODES_REV = {v: k for k, v in DV_MODES.items()}

    INTERFACE_SUPPORT_MAP = {
        0: "Not Supported",
        1: "Supported"
    }
    INTERFACE_SUPPORT_MAP_REV = {v: k for k, v in INTERFACE_SUPPORT_MAP.items()}

    # Color primary integer bit values from the "Player Led (HDR)" BT.2020 example
    # Gx: 0.1700 -> 0101011 (43), Gy: 0.7970 -> 1001100 (76)
    # Rx: 0.7080 -> 10101 (21),  Bx: 0.1310 -> 001 (1)
    # Ry: 0.2920 -> 01010 (10),  By: 0.0460 -> 011 (3)
    COLOR_PRESETS = {
        "BT.2020_Example": { # From the user's "Player Led (HDR)" table
            "gx_bits": 0b0101011, "gy_bits": 0b1001100,
            "rx_bits": 0b10101,   "bx_bits": 0b001,
            "ry_bits": 0b01010,   "by_bits": 0b011
        },
        "BT.709_Example_Placeholder": { # Placeholder, actual bits depend on encoding scheme
            "gx_bits": 0, "gy_bits": 0, "rx_bits": 0, "bx_bits": 0, "ry_bits": 0, "by_bits": 0
        },
        "DCI-P3_Example_Placeholder": { # Placeholder
            "gx_bits": 0, "gy_bits": 0, "rx_bits": 0, "bx_bits": 0, "ry_bits": 0, "by_bits": 0
        }
        # Add more if known bit patterns are available
    }


    def __init__(self, hex_payload: str):
        if len(hex_payload) != 14 or not all(c in '0123456789abcdefABCDEF' for c in hex_payload):
            raise ValueError("Payload must be a 14-character hexadecimal string.")
        self.hex_payload = hex_payload.lower()
        self.bytes = [int(self.hex_payload[i:i+2], 16) for i in range(0, 14, 2)]
        self.decode()

    def decode(self):
        # Byte 1: 48h = 01001000
        self.version_bits = (self.bytes[0] >> 5) & 0b111
        self.dm_version_bits = (self.bytes[0] >> 2) & 0b111
        self.backlight_ctrl_bit = (self.bytes[0] >> 1) & 0b1
        self.yuv_12bit_support_bit = self.bytes[0] & 0b1

        # Byte 2: 03h = 00000011
        self.min_lum_nits_index = (self.bytes[1] >> 3) & 0b11111
        self.global_dimming_bit = (self.bytes[1] >> 2) & 0b1
        self.backlight_min_lum_bits = self.bytes[1] & 0b11

        # Byte 3: 76h = 01110110 (for 480376...) or CAh = 11001010 (for 490BCA...)
        self.max_lum_nits_index = (self.bytes[2] >> 3) & 0b11111
        # The lower 3 bits of byte 2 (index from 0) are DV Mode and Reserved
        # The example 'Original' uses 49 0B CA ... -> CA is byte 2
        # DV Mode bits are the lowest 2 bits of this byte, according to "Original" example where DV Mode "Std + LLDV" (10)
        # matches CAh = 11001010
        # Reserved (bit 2 of byte 2)
        self.reserved_byte2_bit2 = (self.bytes[2] >> 2) & 0b1 # This is the middle bit of the lower 3 bits
        self.dv_mode_bits = self.bytes[2] & 0b11 # Lowest 2 bits

        # Byte 4: 82h = 10000010
        self.gx_bits = (self.bytes[3] >> 1) & 0b1111111
        self.interface_12b_444_support_bit = self.bytes[3] & 0b1

        # Byte 5: 5Eh = 01011110
        self.gy_bits = (self.bytes[4] >> 1) & 0b1111111
        self.interface_10b_444_support_bit = self.bytes[4] & 0b1

        # Byte 6: 6Dh = 01101101
        self.rx_bits = (self.bytes[5] >> 3) & 0b11111
        self.bx_bits = self.bytes[5] & 0b111

        # Byte 7: 95h = 10010101
        self.ry_bits = (self.bytes[6] >> 3) & 0b11111
        self.by_bits = self.bytes[6] & 0b111

    def encode(self) -> str:
        self.bytes[0] = (
            (self.version_bits << 5) |
            (self.dm_version_bits << 2) |
            (self.backlight_ctrl_bit << 1) |
            self.yuv_12bit_support_bit
        )
        self.bytes[1] = (
            (self.min_lum_nits_index << 3) |
            (self.global_dimming_bit << 2) |
            self.backlight_min_lum_bits
        )
        self.bytes[2] = (
            (self.max_lum_nits_index << 3) |
            (self.reserved_byte2_bit2 << 2) | # Preserve reserved bit
            self.dv_mode_bits
        )
        self.bytes[3] = (
            (self.gx_bits << 1) |
            self.interface_12b_444_support_bit
        )
        self.bytes[4] = (
            (self.gy_bits << 1) |
            self.interface_10b_444_support_bit
        )
        self.bytes[5] = (
            (self.rx_bits << 3) |
            self.bx_bits
        )
        self.bytes[6] = (
            (self.ry_bits << 3) |
            self.by_bits
        )
        self.hex_payload = "".join(f"{b:02x}" for b in self.bytes)
        return self.hex_payload

    def get_info(self) -> dict:
        info = {
            "Original Hex Payload": self.hex_payload,
            "Byte 1 (Version, DM Ver, Backlight, YUV)": f"0x{self.bytes[0]:02x}",
            "  Version Bits": f"0b{self.version_bits:03b} ({self.version_bits})",
            "  DM Version Bits": f"0b{self.dm_version_bits:03b} ({self.DM_VERSIONS.get(self.dm_version_bits, 'Unknown')})",
            "  Backlight Ctrl Bit": f"{self.backlight_ctrl_bit} ({self.BACKLIGHT_CTRL_MAP.get(self.backlight_ctrl_bit, 'Unknown')})",
            "  YUV 12-bit Support Bit": f"{self.yuv_12bit_support_bit} ({self.YUV_SUPPORT_MAP.get(self.yuv_12bit_support_bit, 'Unknown')})",

            "Byte 2 (Min Lum, Global Dim, Backlight Min Lum)": f"0x{self.bytes[1]:02x}",
            "  Min Display Luminance Index": f"{self.min_lum_nits_index} ({self.MIN_LUM_NITS_TABLE.get(self.min_lum_nits_index, 'Unknown')} nits)",
            "  Global Dimming Support Bit": f"{self.global_dimming_bit} ({self.GLOBAL_DIMMING_MAP.get(self.global_dimming_bit, 'Unknown')})",
            "  Backlight Min Luminance Bits": f"0b{self.backlight_min_lum_bits:02b} ({self.BACKLIGHT_MIN_LUM_MAP.get(self.backlight_min_lum_bits, 'Unknown')})",

            "Byte 3 (Max Lum, Reserved, DV Mode)": f"0x{self.bytes[2]:02x}",
            "  Max Display Luminance Index": f"{self.max_lum_nits_index} ({self.MAX_LUM_NITS_TABLE.get(self.max_lum_nits_index, 'Unknown')} nits)",
            "  Reserved (Byte 2, Bit 2)": f"{self.reserved_byte2_bit2}",
            "  DV Mode Bits": f"0b{self.dv_mode_bits:02b} ({self.DV_MODES.get(self.dv_mode_bits, 'Unknown')})",

            "Byte 4 (Gx, 12b 444 Support)": f"0x{self.bytes[3]:02x}",
            "  Gx Coordinate Bits": f"0b{self.gx_bits:07b} ({self.gx_bits})",
            "  Interface 12b 4:4:4 Support Bit": f"{self.interface_12b_444_support_bit} ({self.INTERFACE_SUPPORT_MAP.get(self.interface_12b_444_support_bit, 'Unknown')})",

            "Byte 5 (Gy, 10b 444 Support)": f"0x{self.bytes[4]:02x}",
            "  Gy Coordinate Bits": f"0b{self.gy_bits:07b} ({self.gy_bits})",
            "  Interface 10b 4:4:4 Support Bit": f"{self.interface_10b_444_support_bit} ({self.INTERFACE_SUPPORT_MAP.get(self.interface_10b_444_support_bit, 'Unknown')})",

            "Byte 6 (Rx, Bx)": f"0x{self.bytes[5]:02x}",
            "  Rx Coordinate Bits": f"0b{self.rx_bits:05b} ({self.rx_bits})",
            "  Bx Coordinate Bits": f"0b{self.bx_bits:03b} ({self.bx_bits})",

            "Byte 7 (Ry, By)": f"0x{self.bytes[6]:02x}",
            "  Ry Coordinate Bits": f"0b{self.ry_bits:05b} ({self.ry_bits})",
            "  By Coordinate Bits": f"0b{self.by_bits:03b} ({self.by_bits})",
        }
        return info

    def set_dm_version_str(self, version_str: str):
        if version_str in self.DM_VERSIONS_REV:
            self.dm_version_bits = self.DM_VERSIONS_REV[version_str]
        else:
            raise ValueError(f"Invalid DM Version string. Choose from: {list(self.DM_VERSIONS.values())}")

    def set_backlight_ctrl_str(self, ctrl_str: str):
        if ctrl_str in self.BACKLIGHT_CTRL_MAP_REV:
            self.backlight_ctrl_bit = self.BACKLIGHT_CTRL_MAP_REV[ctrl_str]
        else:
            raise ValueError(f"Invalid Backlight Ctrl string. Choose from: {list(self.BACKLIGHT_CTRL_MAP.values())}")

    def set_yuv_support_str(self, support_str: str):
        if support_str in self.YUV_SUPPORT_MAP_REV:
            self.yuv_12bit_support_bit = self.YUV_SUPPORT_MAP_REV[support_str]
        else:
            raise ValueError(f"Invalid YUV Support string. Choose from: {list(self.YUV_SUPPORT_MAP.values())}")

    def set_min_lum_nits_by_value(self, nits_value: float):
        # Find closest nits value in table
        closest_nits = min(self.MIN_LUM_NITS_TABLE.values(), key=lambda x:abs(x-nits_value))
        if abs(closest_nits - nits_value) > 0.0001 : # Allow small tolerance
             print(f"Warning: Exact nits value {nits_value} not found. Using closest: {closest_nits} nits.")
        self.min_lum_nits_index = self.MIN_LUM_NITS_TABLE_REV[closest_nits]


    def set_global_dimming_str(self, dimming_str: str):
        if dimming_str in self.GLOBAL_DIMMING_MAP_REV:
            self.global_dimming_bit = self.GLOBAL_DIMMING_MAP_REV[dimming_str]
        else:
            raise ValueError(f"Invalid Global Dimming string. Choose from: {list(self.GLOBAL_DIMMING_MAP.values())}")

    def set_backlight_min_lum_str(self, lum_str: str):
        if lum_str in self.BACKLIGHT_MIN_LUM_MAP_REV_SET:
            self.backlight_min_lum_bits = self.BACKLIGHT_MIN_LUM_MAP_REV_SET[lum_str]
        else:
            raise ValueError(f"Invalid Backlight Min Lum string. Choose from: {list(self.BACKLIGHT_MIN_LUM_MAP_REV_SET.keys())}")

    def set_max_lum_nits_by_value(self, nits_value: int):
        closest_nits = min(self.MAX_LUM_NITS_TABLE.values(), key=lambda x:abs(x-nits_value))
        if closest_nits != nits_value:
            print(f"Warning: Exact nits value {nits_value} not found. Using closest: {closest_nits} nits.")
        self.max_lum_nits_index = self.MAX_LUM_NITS_TABLE_REV[closest_nits]

    def set_dv_mode_str(self, mode_str: str):
        if mode_str in self.DV_MODES_REV:
            self.dv_mode_bits = self.DV_MODES_REV[mode_str]
        else:
            raise ValueError(f"Invalid DV Mode string. Choose from: {list(self.DV_MODES.values())}")

    def set_interface_12b_444_support_str(self, support_str: str):
        if support_str in self.INTERFACE_SUPPORT_MAP_REV:
            self.interface_12b_444_support_bit = self.INTERFACE_SUPPORT_MAP_REV[support_str]
        else:
            raise ValueError(f"Invalid 12b 4:4:4 Support string. Choose from: {list(self.INTERFACE_SUPPORT_MAP.values())}")

    def set_interface_10b_444_support_str(self, support_str: str):
        if support_str in self.INTERFACE_SUPPORT_MAP_REV:
            self.interface_10b_444_support_bit = self.INTERFACE_SUPPORT_MAP_REV[support_str]
        else:
            raise ValueError(f"Invalid 10b 4:4:4 Support string. Choose from: {list(self.INTERFACE_SUPPORT_MAP.values())}")

    def set_color_primaries_preset(self, preset_name: str):
        if preset_name in self.COLOR_PRESETS:
            preset = self.COLOR_PRESETS[preset_name]
            self.gx_bits = preset["gx_bits"]
            self.gy_bits = preset["gy_bits"]
            self.rx_bits = preset["rx_bits"]
            self.bx_bits = preset["bx_bits"]
            self.ry_bits = preset["ry_bits"]
            self.by_bits = preset["by_bits"]
        else:
            raise ValueError(f"Invalid color preset name. Choose from: {list(self.COLOR_PRESETS.keys())}")

# --- Command Line Interface ---

def display_info(vsvdb: DolbyVisionVSVDB):
    info = vsvdb.get_info()
    print("\n--- Current VSVDB Information ---")
    for key, value in info.items():
        print(f"{key}: {value}")
    print("---------------------------------")

def get_int_choice(prompt, min_val, max_val):
    while True:
        try:
            choice = int(input(prompt))
            if min_val <= choice <= max_val:
                return choice
            else:
                print(f"Invalid choice. Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_str_choice(prompt, options_dict):
    print(prompt)
    options_list = list(options_dict.values()) if isinstance(options_dict, dict) else list(options_dict)
    for i, option in enumerate(options_list):
        print(f"  {i+1}. {option}")
    while True:
        try:
            choice_num = int(input("Enter choice number: ")) -1
            if 0 <= choice_num < len(options_list):
                return options_list[choice_num]
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(options_list)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_int_input(prompt, max_bits=None):
    while True:
        try:
            val = int(input(prompt))
            if max_bits:
                max_val = (1 << max_bits) -1
                if 0 <= val <= max_val:
                    return val
                else:
                    print(f"Value out of range (0 to {max_val} for {max_bits} bits).")
            else:
                return val
        except ValueError:
            print("Invalid input. Please enter an integer.")


def modify_menu(vsvdb: DolbyVisionVSVDB):
    while True:
        print("\n--- Modify VSVDB Fields ---")
        fields = [
            "Version Bits (0-7)", "DM Version", "Backlight Control", "YUV 12-bit Support",
            "Min Display Luminance (nits)", "Global Dimming Support", "Backlight Min Luminance",
            "Max Display Luminance (nits)", "DV Mode",
            "Gx Coordinate Bits (0-127)", "Interface 12b 4:4:4 Support",
            "Gy Coordinate Bits (0-127)", "Interface 10b 4:4:4 Support",
            "Rx Coordinate Bits (0-31)", "Bx Coordinate Bits (0-7)",
            "Ry Coordinate Bits (0-31)", "By Coordinate Bits (0-7)",
            "Set Color Primaries from Preset",
            "Back to Main Menu"
        ]
        for i, field in enumerate(fields):
            print(f"{i+1}. {field}")

        choice = get_int_choice("Select field to modify: ", 1, len(fields))

        try:
            if choice == 1:
                vsvdb.version_bits = get_int_input("Enter Version bits (0-7, 3 bits): ", max_bits=3)
            elif choice == 2:
                vsvdb.set_dm_version_str(get_str_choice("Select DM Version:", vsvdb.DM_VERSIONS))
            elif choice == 3:
                vsvdb.set_backlight_ctrl_str(get_str_choice("Select Backlight Control:", vsvdb.BACKLIGHT_CTRL_MAP))
            elif choice == 4:
                vsvdb.set_yuv_support_str(get_str_choice("Select YUV 12-bit Support:", vsvdb.YUV_SUPPORT_MAP))
            elif choice == 5:
                nits = get_float_input(f"Enter Min Display Luminance (nits, e.g., 0.001). Current values: {sorted(list(vsvdb.MIN_LUM_NITS_TABLE.values()))[:5]}...: ")
                vsvdb.set_min_lum_nits_by_value(nits)
            elif choice == 6:
                vsvdb.set_global_dimming_str(get_str_choice("Select Global Dimming Support:", vsvdb.GLOBAL_DIMMING_MAP))
            elif choice == 7:
                vsvdb.set_backlight_min_lum_str(get_str_choice("Select Backlight Min Luminance:", vsvdb.BACKLIGHT_MIN_LUM_MAP_REV_SET)) # use rev_set for distinct options
            elif choice == 8:
                nits = get_int_input(f"Enter Max Display Luminance (nits, e.g., 1000). Current values: {sorted(list(vsvdb.MAX_LUM_NITS_TABLE.values()))[:5]}...: ")
                vsvdb.set_max_lum_nits_by_value(nits)
            elif choice == 9:
                vsvdb.set_dv_mode_str(get_str_choice("Select DV Mode:", vsvdb.DV_MODES))
            elif choice == 10:
                vsvdb.gx_bits = get_int_input("Enter Gx Coordinate bits (0-127, 7 bits): ", max_bits=7)
            elif choice == 11:
                vsvdb.set_interface_12b_444_support_str(get_str_choice("Select Interface 12b 4:4:4 Support:", vsvdb.INTERFACE_SUPPORT_MAP))
            elif choice == 12:
                vsvdb.gy_bits = get_int_input("Enter Gy Coordinate bits (0-127, 7 bits): ", max_bits=7)
            elif choice == 13:
                vsvdb.set_interface_10b_444_support_str(get_str_choice("Select Interface 10b 4:4:4 Support:", vsvdb.INTERFACE_SUPPORT_MAP))
            elif choice == 14:
                vsvdb.rx_bits = get_int_input("Enter Rx Coordinate bits (0-31, 5 bits): ", max_bits=5)
            elif choice == 15:
                vsvdb.bx_bits = get_int_input("Enter Bx Coordinate bits (0-7, 3 bits): ", max_bits=3)
            elif choice == 16:
                vsvdb.ry_bits = get_int_input("Enter Ry Coordinate bits (0-31, 5 bits): ", max_bits=5)
            elif choice == 17:
                vsvdb.by_bits = get_int_input("Enter By Coordinate bits (0-7, 3 bits): ", max_bits=3)
            elif choice == 18:
                vsvdb.set_color_primaries_preset(get_str_choice("Select Color Primaries Preset:", vsvdb.COLOR_PRESETS))
            elif choice == len(fields):
                break # Back to main menu
            
            vsvdb.encode() # Re-encode after modification
            print("Field updated.")
            display_info(vsvdb) # Show updated info

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def main_cli():
    print("Welcome to the Dolby Vision VSVDB Tool!")
    current_payload_hex = ""
    vsvdb = None

    while True:
        if not vsvdb:
            while True:
                payload_input = input("Enter 7-byte VSVDB hex payload (e.g., 480376825e6d95) or press Enter for default: ").strip().lower()
                if not payload_input:
                    payload_input = "480376825e6d95" # Default example
                if len(payload_input) == 14 and all(c in '0123456789abcdef' for c in payload_input):
                    current_payload_hex = payload_input
                    try:
                        vsvdb = DolbyVisionVSVDB(current_payload_hex)
                        print(f"Loaded payload: {vsvdb.hex_payload}")
                        break
                    except ValueError as e:
                        print(f"Error initializing VSVDB: {e}")
                        vsvdb = None # Reset vsvdb
                else:
                    print("Invalid payload format. Must be 14 hex characters.")
        
        if not vsvdb: # Should not happen if loop above works, but as a safe guard
            print("Failed to load a VSVDB. Exiting.")
            return

        print("\n--- Main Menu ---")
        print("1. Show Current VSVDB Info")
        print("2. Modify VSVDB Fields")
        print("3. Show Raw Hex Payload")
        print("4. Load New Payload")
        print("5. Exit")

        choice = get_int_choice("Enter your choice: ", 1, 5)

        if choice == 1:
            display_info(vsvdb)
        elif choice == 2:
            modify_menu(vsvdb)
        elif choice == 3:
            print(f"\nCurrent Raw Hex Payload: {vsvdb.encode()}")
        elif choice == 4:
            vsvdb = None # Force reload
        elif choice == 5:
            print("Exiting tool.")
            break

if __name__ == '__main__':
    main_cli()