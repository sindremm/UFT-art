import tkinter as tk
from tkinter import filedialog
from PIL import Image
import numpy as np


def get_img():
    """Open a file dialog to select an image file with standard size."""
    root = tk.Tk()
    root.withdraw()
    root.geometry("600x450")
    img_file = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tif *.tiff")]
    )
    root.destroy()
    return img_file


def to_img(img_file):
    """Read an image file and return it as a grayscale numpy array."""
    image = Image.open(img_file).convert('L')
    return np.array(image)


def show_img(name, img):
    """Display an image in a window using PIL with standard size."""
    img_pil = Image.fromarray(img)
    img_pil.show(title=name)


def add_to_clipboard(text):
    """Copy text to the clipboard using tkinter."""
    if not text:
        return
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    root.destroy()


def average_square(image, pos, size):
    """Calculate the average pixel value in a square region of the image."""
    pixel_list = []
    for y in range(size):
        for x in range(size):
            pixel_list.append(image[pos[0] + x][pos[1] + y])
    
    avg_level = np.average(pixel_list)
    return avg_level


def set_square(image, pos, size, value):
    """Set all pixels in a square region to a given value."""
    new_image = image.copy()
    for y in range(size):
        for x in range(size):
            new_image[pos[0] + x][pos[1] + y] = value
    return new_image


def set_value(pixel_img, pos, value):
    """Set a single pixel value in the image."""
    pixel_img[pos[0]][pos[1]] = value


def pixelate(img, pixelation):
    """
    Pixelate an image by averaging pixel values in square blocks.

    Args:
        img: Input grayscale image as numpy array
        pixelation: Size of the pixelation block

    Returns:
        Pixelated image as numpy array
    """
    height, width = img.shape
    new_height = height - (height % pixelation)
    new_width = width - (width % pixelation)
    
    pixelated_img = np.zeros((new_height, new_width), np.uint8)
    value_img = np.zeros((new_height // pixelation, new_width // pixelation), np.uint8)

    for n in range(0, new_height, pixelation):
        for k in range(0, new_width, pixelation):
            avg = average_square(img, [n, k], pixelation)
            pixelated_img = set_square(pixelated_img, [n, k], pixelation, avg)
            set_value(value_img, [n // pixelation, k // pixelation], avg)
    
    return pixelated_img


# UTF-8 character mapping for different grayscale levels
UTF_CHAR_MAP = {
    0: " ",
    10: "¨",
    20: "'",
    30: "`",
    40: "-",
    50: ":",
    60: "^",
    70: "*",
    80: ">",
    90: "+",
    100: "=",
    110: "!",
    120: "\\",
    130: "|",
    140: "?",
    150: "x",
    160: "¤",
    170: "#",
    180: "£",
    190: "%",
    200: "8",
    210: "0",
    220: "§",
    230: "Æ",
    240: "&",
    250: "@",
    260: "Ø"
}


def int_to_char(number):
    """
    Convert a pixel value (0-255) to a corresponding UTF-8 character.

    Args:
        number: Pixel intensity value (0 = black, 255 = white)

    Returns:
        UTF-8 character representing the intensity
    """
    convert_number = round(260 - int(number), -1)
    convert_number = max(0, min(260, convert_number))
    return UTF_CHAR_MAP.get(convert_number, " ")


def to_utf(raw_img, pixelation):
    """
    Convert a pixelated image to a UTF-8 string representation.
    Each character is duplicated to double the width of the output.

    Args:
        raw_img: Input grayscale image as numpy array
        pixelation: Size of the pixelation block

    Returns:
        String containing UTF-8 characters representing the image
    """
    utf_string = ""
    for row in raw_img[::pixelation]:
        string_row = [int_to_char(pixel) for pixel in row[::pixelation]]
        doubled_row = "".join([char * 2 for char in string_row])
        utf_string += doubled_row + "\n"
    return utf_string


if __name__ == "__main__":
    im = to_img(get_img())
    show_img("Original", im)
    pixel_img = pixelate(im, 3)
    show_img("Pixelated", pixel_img)
    utf = to_utf(pixel_img, 3)
    add_to_clipboard(utf)
