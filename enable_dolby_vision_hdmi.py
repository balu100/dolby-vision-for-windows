import sys


def hex_to_int(hex: str):
  return int(hex, 16)


def int_to_hex(num: int):
  return f'{num:x}'


def enable_dolby_vision_hdmi(hex: str):
  assert len(hex) == 14
  hex_chunks_index = 2  # the index containing the dolby vision values

  # split into chunks of 2 characters
  hex_chunks = [hex[i : i + 2] for i in range(0, len(hex), 2)]

  # set the last bit to enable 'LLDV-HDMI'
  dolby_bits = hex_to_int(hex_chunks[hex_chunks_index])
  dolby_bits |= 1

  hex_chunks[hex_chunks_index] = int_to_hex(dolby_bits)
  return ''.join(hex_chunks)


def run_tests():
  samples = (
    ('480376825e6d95', '480377825e6d95'),  # https://github.com/balu100/dolby-vision-for-windows/blob/e393cbb47571e9053db4273e1cd62bb6ce162a21/README.md?plain=1#L23
    ('4403609248458f', '4403619248458f'),  # https://github.com/balu100/dolby-vision-for-windows/issues/1#issuecomment-2188170968
    ('4d4e4a725a7776', '4d4e4b725a7776'),  # https://github.com/balu100/dolby-vision-for-windows/issues/2#issue-2506429409
    ('480a7e86607694', '480a7f86607694'),  # https://github.com/balu100/dolby-vision-for-windows/issues/2#issuecomment-2330407252
    ('48039e5898aa5c', '48039f5898aa5c'),  # https://github.com/balu100/dolby-vision-for-windows/issues/2#issuecomment-2330708632
  )
  for hex_input, expected_hex_output in samples:
    hex_output = enable_dolby_vision_hdmi(hex_input)
    assert hex_output == expected_hex_output


def main():
  try:
    video_hex = sys.argv[1]
  except IndexError:
    video_hex = None
  else:
    video_hex = video_hex.strip()

  if not video_hex:
    raise ValueError('No value provided for argument `video_hex`')

  new_video_hex = enable_dolby_vision_hdmi(video_hex)
  if new_video_hex == video_hex:
    print("Warning: `video_hex` of '%s' is already enabled with LLDV-HDMI" % video_hex)
  else:
    print("Update `video_hex` from '%s' to '%s' to enable LLDV-HDMI" % (video_hex, new_video_hex))


if __name__ == '__main__':
  main()
