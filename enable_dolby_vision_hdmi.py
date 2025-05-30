import sys

def hex_to_int(hex_str: str) -> int:
    """Convert a hexadecimal string to an integer."""
    return int(hex_str, 16)

def int_to_hex(num: int) -> str:
    """Convert an integer to a 2-character hexadecimal string."""
    return f'{num:02x}'

def enable_dolby_vision_hdmi(hex_str: str) -> str:
    """
    Enable Dolby Vision HDMI by modifying the appropriate byte in a 14-character
    hexadecimal string.
    """
    if len(hex_str) != 14 or not all(c in '0123456789abcdefABCDEF' for c in hex_str):
        raise ValueError("Error: Input must be a 14-character hexadecimal string.")
    
    hex_chunks_index = 2  # Index of the Dolby Vision value in the chunks

    # Split into chunks of 2 characters
    hex_chunks = [hex_str[i : i + 2] for i in range(0, len(hex_str), 2)]

    # Set the last bit to enable 'LLDV-HDMI'
    dolby_bits = hex_to_int(hex_chunks[hex_chunks_index])
    dolby_bits |= 1  # Enable the last bit
    hex_chunks[hex_chunks_index] = int_to_hex(dolby_bits)

    return ''.join(hex_chunks)

def run_tests():
    """Run test cases to validate the enable_dolby_vision_hdmi function."""
    samples = (
        ('480376825e6d95', '480377825e6d95'),
        ('4403609248458f', '4403619248458f'),
        ('4d4e4a725a7776', '4d4e4b725a7776'),
        ('480a7e86607694', '480a7f86607694'),
        ('48039e5898aa5c', '48039f5898aa5c'),
    )
    for hex_input, expected_hex_output in samples:
        hex_output = enable_dolby_vision_hdmi(hex_input)
        assert hex_output == expected_hex_output, (
            f"Test failed: {hex_input} -> {hex_output} (expected {expected_hex_output})"
        )
    print("All tests passed.")

def main():
    """Main function to handle command-line input."""
    if len(sys.argv) < 2:
        print("Error: No input provided. Please enter a 14-character hexadecimal string.")
        sys.exit(1)

    video_hex = sys.argv[1].strip()

    if len(video_hex) != 14 or not all(c in '0123456789ABCDEFabcdef' for c in video_hex):
        print("Error: Invalid hexadecimal input! Must be exactly 14 characters.")
        sys.exit(1)

    new_video_hex = enable_dolby_vision_hdmi(video_hex)
    
    if new_video_hex == video_hex:
        print(f"Warning: `video_hex` of '{video_hex}' is already enabled with LLDV-HDMI")
    else:
        print(f"Update `video_hex` from '{video_hex}' to '{new_video_hex}' to enable LLDV-HDMI")

if __name__ == '__main__':
    run_tests()
    main()
