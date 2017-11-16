import time

from skimage import img_as_ubyte
from skimage import io
from skimage.transform import resize


def loadAndTransform():
    img1 = io.imread("D:/FeatureHashing/pepe1.jpg", as_grey=True)
    img2 = io.imread("D:/FeatureHashing/pepe2.jpg", as_grey=True)
    img1_resized = resize(img1, (8, 9))
    img2_resized = resize(img2, (8, 9))
    return (img_as_ubyte(img1_resized), img_as_ubyte(img2_resized))

def booleanizePicture(pictureArray):
    booleanized = []
    for row in pictureArray:
        booleanizedRow = []
        rowSize = len(row)
        for index, value in enumerate(row):
            if index + 1 < rowSize:
                if row[index] > row[index + 1]:
                    booleanizedRow.append(True)
                else:
                    booleanizedRow.append(False)
        booleanized.append(booleanizedRow)
    return booleanized

# Copyright to David Kofoed Wind
def hashh(booleanizedImageArray):
    hex_string = []
    for difference in booleanizedImageArray:
        decimal_value = 0
        for index, value in enumerate(difference):
            if value:
                decimal_value += 2 ** (index % 8)
            if (index % 8) == 7:
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value = 0
    print(''.join(hex_string))

if __name__ == '__main__':
    start_time = time.time()
    img1, img2 = loadAndTransform()
    img1_booleanized = booleanizePicture(img1)
    img2_booleanized = booleanizePicture(img2)
    hashh(img1_booleanized)
    hashh(img2_booleanized)

    print("Execution time: %s seconds." % (time.time() - start_time))