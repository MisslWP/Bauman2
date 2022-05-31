from struct import pack, unpack


def toBits(n: int):
    bits = []
    for i in range(8):
        bits.append(0 if (n & (2 ** i)) == 0 else 1)
    return bits


def from_bits(bits: list) -> int:
    res = 0
    for i in range(8):
        res += bits[i] * (2 ** i)
    return res


class EncodedBitmap:
    def __init__(self, bfType, bfReserved1, bfReserved2, bcPlanes, bcSize, bcBitCount, bfOffBits, bcWidth, bcHeight,
                 bfSize, grapichs, extra=b'', raw_inf=b'', clear=False):
        self._bfType = bfType
        self._bfReserved1 = bfReserved1
        self._bfReserved2 = bfReserved2
        self._bcPlanes = bcPlanes
        self._bcSize = bcSize
        self._bcBitCount = bcBitCount
        self._bfOffBits = bfOffBits
        self._bcWidth = bcWidth
        self._bcHeight = bcHeight
        self._bfSize = bfSize
        self._graphics = grapichs
        self.extra_bytes = extra
        self.raw_info = raw_inf
        if clear:
            self.clear()

    @staticmethod
    def gen_new(width, height):
        return EncodedBitmap(19778, 0, 0, 1, 12, 24, 26, width, height, 26 + width * 3 * height, [], clear=True)

    @staticmethod
    def from_file(path: str):
        with open(path, 'rb') as f:
            hdr = unpack('<HLHHL', f.read(14))
            raw_inf_start = f.read(12)
            inf = unpack('<LHHHH', raw_inf_start)
            pixels = []
            extra = f.read(hdr[4]-26)
            while (pix := f.read(3)) != b'':
                pixels.append(unpack('<BBB', pix))
            if hdr[4] == 26:
                return EncodedBitmap(hdr[0], hdr[2], hdr[3], inf[3], inf[0], inf[4], hdr[4], inf[1], inf[2], hdr[1], pixels, extra)
            else:
                return EncodedBitmap(hdr[0], hdr[2], hdr[3], inf[3], inf[0], inf[4], hdr[4], inf[1], inf[3], hdr[1], pixels, extra, raw_inf_start)

    def get_ascii_text(self):
        pixel_data = []
        for x in range(self._bcWidth):
            for y in range(self._bcHeight):
                (b, g, r) = self.getPixel(x, y)
                pixel_data.append((g & 1, b & 1))
        all_bits = []
        for i in range(self.get_max_message_size()):
            (b0, b1) = pixel_data[4 * i + 0]
            (b2, b3) = pixel_data[4 * i + 1]
            (b4, b5) = pixel_data[4 * i + 2]
            (b6, b7) = pixel_data[4 * i + 3]
            all_bits.append([b0, b1, b2, b3, b4, b5, b6, b7])
        all_data = list(map(from_bits, all_bits))
        bt_arr = bytearray()
        for b in all_data:
            if b == 0:
                break
            bt_arr.append(b)
        try:
            return bt_arr.decode('ascii')
        except UnicodeDecodeError:
            return ''

    def set_ascii_text(self, text: str):
        data = text.encode('ascii')
        if len(data) >= self.get_max_message_size():
            raise ValueError('Data size is more than image can hold!')
        pixel_data = []
        for b in data:
            bits = toBits(b)
            pixel_data.append((bits[0], bits[1]))
            pixel_data.append((bits[2], bits[3]))
            pixel_data.append((bits[4], bits[5]))
            pixel_data.append((bits[6], bits[7]))
        pixel_data.append((0, 0))
        pixel_data.append((0, 0))
        pixel_data.append((0, 0))
        pixel_data.append((0, 0))
        breakFlag = False
        for x in range(self._bcWidth):
            if breakFlag:
                break
            for y in range(self._bcHeight):
                if len(pixel_data) == 0:
                    breakFlag = True
                    break
                pix = self.getPixel(x, y)
                (r, g, b) = pix
                data = pixel_data.pop(0)
                g = (g & 254) + data[0]
                b = (b & 254) + data[1]
                self.setPixel(x, y, (r, g, b))

    def get_max_message_size(self):
        return int(self._bcWidth * self._bcHeight / 4)

    def clear(self):
        self._graphics = [(0, 0, 0)] * self._bcWidth * self._bcHeight

    def getPixel(self, x, y):
        return self._graphics[y * self._bcWidth + x]

    def setPixel(self, x, y, color):
        self._graphics[y * self._bcWidth + x] = (color[2], color[1], color[0])

    def write(self, file):
        with open(file, 'wb') as f:
            f.write(pack('<HLHHL',
                         self._bfType,
                         self._bfSize,
                         self._bfReserved1,
                         self._bfReserved2,
                         self._bfOffBits))  # Writing BITMAPFILEHEADER
            if self._bfOffBits == 26:
                f.write(pack('<LHHHH',
                         self._bcSize,
                         self._bcWidth,
                         self._bcHeight,
                         self._bcPlanes,
                         self._bcBitCount))  # Writing BITMAPINFO
            else:
                f.write(self.raw_info)
            f.write(self.extra_bytes)
            for px in self._graphics:
                f.write(pack('<BBB', *px))
            for i in range((4 - ((self._bcWidth * 3) % 4)) % 4):
                f.write(pack('B', 0))


def text_from_file(path: str):
    bmp = EncodedBitmap.from_file(path)
    return bmp.get_ascii_text()


def save_with_text(path_from: str, path_to: str, text: str):
    bmp = EncodedBitmap.from_file(path_from)
    bmp.set_ascii_text(text)
    bmp.write(path_to)
