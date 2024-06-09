from PIL import Image

class rtw_image:
    def __init__(self, filename):
        self.image = Image.open(filename)

    def width(self):
        return self.image.width

    def height(self):
        return self.image.height

    def pixel_data(self, i, j):
        return self.image.getpixel((i, j))

# Example usage:
if __name__ == "__main__":
    img = rtw_image("earthmap.jpg")
    print("Image Width:", img.width())
    print("Image Height:", img.height())
    print("Pixel Data (0, 0):", img.pixel_data(0, 0))
