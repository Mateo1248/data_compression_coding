from pixel_map import PixelMap


def extract_header(file):
    header = {}
    header['id-length'] = file.read(1)[0]
    header['color-map-type'] = file.read(1)[0]
    header['image-type'] = file.read(1)[0]
    header['color-map-first-entry-index'] = file.read(1)[0] + (file.read(1)[0] << 8)
    header['color-map-length'] = file.read(1)[0] + (file.read(1)[0] << 8)
    header['color-map-entry-size'] = file.read(1)[0]
    header['x-origin'] = file.read(1)[0] + (file.read(1)[0] << 8)
    header['y-origin'] = file.read(1)[0] + (file.read(1)[0] << 8)
    header['width'] = file.read(1)[0] + (file.read(1)[0] << 8)
    header['height'] = file.read(1)[0] + (file.read(1)[0] << 8)
    header['pixel-depth'] = file.read(1)[0]
    header['descriptor'] = file.read(1)[0]
    return header


def read_image(file, height, width):
    pixel_map = PixelMap(height, width)
    for row in range(height-1, -1, -1):
        for col in range(width):
            blue = file.read(1)[0]
            green = file.read(1)[0]
            red = file.read(1)[0]
            pixel_map.new_pixel(row, col, red, green, blue)
    
    return pixel_map


def extract_footer(file):
    footer = b''
    b = file.read(1)
    while b != b'':
        footer += b
        b = file.read(1)

    return footer


class TGAReader:
    """
        Reader of TGA files.
    """

    def __init__(self, filename):
        self.filename = filename
        self.header, self.pixel_map, self.footer = self.read_file()


    def read_file(self):
        with open(self.filename, 'rb') as file:
            header = extract_header(file)
            assert header['id-length'] == header['color-map-length'] == 0, "ID or Color Map length > 0"
            assert header['pixel-depth'] == 24, "Pixel depth != 24 (3 bytes)"
            pixel_map = read_image(file, header['height'], header['width'])
            footer = extract_footer(file)
        return header, pixel_map, footer


def write_tga(filename, header, pixel_map, footer):
    with open(filename, 'wb') as file:
        for k, entry in header.items():
            if k in ('color-map-first-entry-index', 'color-map-length', 'width', 'height', 'x-origin', 'y-origin'):
                file.write(bytes((entry%256, entry//256)))
            else:
                file.write(bytes((entry,)))
        for row_idx in range(len(pixel_map.pixels)-1, -1, -1):
            for pixel in pixel_map.pixels[row_idx]:
                file.write(bytes((pixel.blue, pixel.green, pixel.red)))
        file.write(footer)


def taxicab_norm(vector):
    return sum(abs(vector))


def get_distance(x, r):
    return sum(taxicab_norm(x - r))


def get_closest_vector(vector, codebook, m=-1):
    if m == -1:
        m = len(codebook)
    return min(map(lambda c: (get_distance(vector, c[1]), c[0]), enumerate(codebook[:m])))