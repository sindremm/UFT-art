import tkinter as tk
from PIL import ImageTk, Image, ImageFilter
from processing import get_img, add_to_clipboard, pixelate, to_utf
import numpy as np


class ImageUi(tk.Tk):
    """Main application window for the UTF image generator."""

    def __init__(self, width, height):
        super().__init__()
        super().title("UTF image generator")
        super().resizable(False, False)

        self.url = None
        self.image = None
        self.pixel_image = None
        self.utf_string = None
        self.imageWidth = width
        self.imageHeight = height

        self.canvas1 = tk.Canvas(self, width=width, height=height, bg="gray")
        self.canvas2 = tk.Canvas(self, width=width, height=height, bg="gray")

        max_pixel_size = min(self.imageWidth // 10, self.imageHeight // 10)
        self.slider = tk.Scale(
            self,
            from_=1,
            to=max_pixel_size,
            orient=tk.HORIZONTAL,
            label="Set pixel size"
        )

        self.canvas1.grid(row=0, column=0, columnspan=2)
        self.canvas2.grid(row=0, column=2, columnspan=2)

        self.slider.grid(row=1, column=1, sticky=tk.EW)

        self.show_pixel_button = tk.Button(
            self,
            text="Pixelate",
            command=lambda: self.setup()
        )
        self.show_pixel_button.grid(row=1, column=2, sticky=tk.NSEW)

        self.clipboard_button = tk.Button(
            self,
            text="Add to clipboard",
            command=lambda: add_to_clipboard(self.utf_string)
        )
        self.clipboard_button.grid(row=1, column=3, sticky=tk.NSEW)

        self.pick_image_button = tk.Button(
            self,
            text="Choose image",
            command=lambda: self.choose_image()
        )
        self.pick_image_button.grid(row=1, column=0, sticky=tk.NSEW)

        self.canvas1_img = self.canvas1.create_image(
            0, 0,
            anchor=tk.NW,
            image=self.image
        )
        self.canvas2_img = self.canvas2.create_image(
            0, 0,
            anchor=tk.NW,
            image=self.image
        )

    def choose_image(self):
        """Open a file dialog and load the selected image."""
        img_path = get_img()
        if not img_path:
            return
        self.pilImg = Image.open(img_path)
        self.pilImg = self.pilImg.resize(
            (self.imageWidth, self.imageHeight),
            Image.Resampling.LANCZOS
        )
        self.image = ImageTk.PhotoImage(self.pilImg)
        self.canvas1.itemconfig(self.canvas1_img, image=self.image)

    def set_image(self):
        """Update the canvas with the pixelated image."""
        new_img = Image.fromarray(self.pixel_image)
        new_img = new_img.resize(
            (self.imageWidth, self.imageHeight),
            Image.Resampling.LANCZOS
        )
        self.pixel_image = ImageTk.PhotoImage(new_img)
        self.canvas2.itemconfig(self.canvas2_img, image=self.pixel_image)

    def setup(self):
        """Process the image: pixelate and convert to UTF."""
        if self.pilImg is None:
            return
        temp_img = np.asarray(self.pilImg.convert('L'))
        pixel_size = int(self.slider.get())
        self.pixel_image = pixelate(temp_img, pixel_size)
        self.utf_string = to_utf(self.pixel_image, pixel_size)
        self.set_image()


if __name__ == "__main__":
    pass
