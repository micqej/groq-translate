"""Create 22x22 template PNG icon for macOS menu bar."""
import struct, zlib

def png(w, h, rows):
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t+d)&0xffffffff)
    raw = b''.join(b'\x00'+bytes(sum(([r,g,b] for r,g,b in row), [])) for row in rows)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB',w,h,8,2,0,0,0)) + chunk(b'IDAT',zlib.compress(raw)) + chunk(b'IEND',b'')

W, H = 22, 22
B = (0, 0, 0)
T = (255, 255, 255)

# Grid: translate arrows icon (two lines + bidirectional arrow)
G = [
    "0000000000000000000000",
    "0000000000000000000000",
    "0011111111110000000000",
    "0011111111110000000000",
    "0000000000000000000000",
    "0011111111000000000000",
    "0011111111000000000000",
    "0000000000000000000000",
    "0000001111000000000000",
    "0000000011110000000000",
    "0011111111110000000000",
    "0011111111110000000000",
    "0000000011110000000000",
    "0000001111000000000000",
    "0000000000000000000000",
    "0000001111111110000000",
    "0000001111111110000000",
    "0000000000000000000000",
    "0011111111110000000000",
    "0011111111110000000000",
    "0000000000000000000000",
    "0000000000000000000000",
]

pixels = [[B if G[y][x]=='1' else T for x in range(W)] for y in range(H)]

with open("menubar_icon.png", "wb") as f:
    f.write(png(W, H, pixels))
print("icon created")
