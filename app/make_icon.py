"""Creates a clean 22x22 menu bar icon as PNG."""
import struct, zlib

def make_png(width, height, pixels):
    def chunk(name, data):
        c = zlib.crc32(name + data) & 0xffffffff
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', c)

    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    raw = b''
    for row in pixels:
        raw += b'\x00'
        for r, g, b in row:
            raw += bytes([r, g, b])

    idat = zlib.compress(raw)
    return (
        b'\x89PNG\r\n\x1a\n' +
        chunk(b'IHDR', ihdr) +
        chunk(b'IDAT', idat) +
        chunk(b'IEND', b'')
    )

W, H = 22, 22
B = (0, 0, 0)       # black
T = (255, 255, 255) # transparent (will be white = template)

def px(x, y, grid):
    if 0 <= y < len(grid) and 0 <= x < len(grid[y]):
        return B if grid[y][x] == '#' else T
    return T

# 22x22 translate icon: two horizontal lines with arrow between
icon = [
    "                      ",
    "                      ",
    "  ##########          ",
    "  ##########          ",
    "                      ",
    "  ######              ",
    "  ######              ",
    "                      ",
    "        ####          ",
    "          ####        ",
    "   ##########         ",
    "    #########         ",
    "          ####        ",
    "        ####          ",
    "                      ",
    "          ######      ",
    "          ######      ",
    "                      ",
    "   ##########         ",
    "   ##########         ",
    "                      ",
    "                      ",
]

pixels = [[px(x, y, icon) for x in range(W)] for y in range(H)]
png_data = make_png(W, H, pixels)

with open("menubar_icon.png", "wb") as f:
    f.write(png_data)

print("menubar_icon.png created")
