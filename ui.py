import tkinter as tk
from PIL import ImageTk, Image, ImageFilter
from processing import get_img, add_to_clipboard, pixelate, to_utf
import numpy as np


class ImageUi(tk.Tk):
    """Main application window for the UTF image generator."""

    def __init__(self, width, height):
        super().__init__()
        super().title("UTF image generator")
        super().resizable(True, True)
        super().geometry("800x600")

        self.url = None
        self.image = None
        self.pixel_image = None
        self.utf_string = None
        self.imageWidth = width
        self.imageHeight = height
        self.original_pilImg = None
        self.original_pixel_image = None

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

        self.canvas1.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        self.canvas2.grid(row=0, column=2, columnspan=2, sticky=tk.NSEW)

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

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """Handle window resize to maintain image aspect ratios."""
        width = event.width
        height = event.height

        canvas_width = (width - 4) // 2
        canvas_height = height - 50

        self.canvas1.config(width=canvas_width, height=canvas_height)
        self.canvas2.config(width=canvas_width, height=canvas_height)

        if self.original_pilImg is not None:
            self.update_image_display()

    def update_image_display(self):
        """Update both canvas images with properly scaled versions."""
        canvas_width = self.canvas1.winfo_width()
        canvas_height = self.canvas1.winfo_height()

        if canvas_width <= 0 or canvas_height <= 0:
            return

        if self.original_pilImg is not None:
            img = self.original_pilImg.copy()
            img.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            self.image = ImageTk.PhotoImage(img)
            self.canvas1.itemconfig(self.canvas1_img, image=self.image)

        if self.original_pixel_image is not None:
            img_array = self.original_pixel_image
            img = Image.fromarray(img_array)
            img.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            self.pixel_image_display = ImageTk.PhotoImage(img)
            self.canvas2.itemconfig(self.canvas2_img, image=self.pixel_image_display)

    def choose_image(self):
        """Open a file dialog and load the selected image."""
        img_path = get_img()
        if not img_path:
            return
        self.original_pilImg = Image.open(img_path)
        self.update_image_display()

    def set_image(self):
        """Update the canvas with the pixelated image."""
        self.update_image_display()

    def setup(self):
        """Process the image: pixelate and convert to UTF."""
        if self.original_pilImg is None:
            return
        temp_img = np.asarray(self.original_pilImg.convert('L'))
        pixel_size = int(self.slider.get())
        self.original_pixel_image = pixelate(temp_img, pixel_size)
        self.utf_string = to_utf(self.original_pixel_image, pixel_size)
        self.update_image_display()


if __name__ == "__main__":
    pass
