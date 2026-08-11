from ui import ImageUi


def start_program():
    """Start the UTF image generator application."""
    root = ImageUi(400, 600)
    root.configure(background="gray")
    root.mainloop()


if __name__ == "__main__":
    start_program()