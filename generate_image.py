from itertools import islice
import numpy as np
from PIL import Image


n = 1860000
filename = 'out.txt'
image_range = np.array([[-2.0, 2.0], [-2.0, 2.0]])
pixels = 1024


def generate_hist(data):
    return np.histogram2d(
        data[:, 1], data[:, 0],
        range=image_range, bins=pixels
    )[0]

def parse_to_numbers(chunk):
    roots = []
    for c in chunk:
        if ' ' not in c:
            roots.append((float(c), 0))
        else:
            parts = c.split()
            r = float(parts[0])
            i = float(''.join(parts[1:])[:-1])
            roots.append((r, i))
    return np.array(roots)


def main():
    with open(filename, 'r') as f:
        histogram = np.zeros((pixels, pixels))
        while True:
            chunk = list(islice(f, n))
            if not chunk: break
            data = parse_to_numbers(chunk)
            histogram += generate_hist(data)

    histogram = histogram * 4
    histogram = np.clip(np.log(histogram + 1) * 2 / np.log(histogram.max() + 1), 0, 1)
    histogram = (np.stack((histogram, histogram, histogram), axis=2) * 255).astype('uint8')
    im = Image.fromarray(histogram)
    im.save('image.tif')


main()
