import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import cv2
import triangler


root = tk.Tk()
root.title("Generate triangulation art from images")
root.geometry("1100x600")


def open():
    global my_image
    filename = filedialog.askopenfilename(initialdir="images",
                                          title="Select A File",
                                          filetypes=(("jpg files", "*.jpg"),
                                                     ("all files", "*.*")))
    my_label.config(text=filename)
    my_image = Image.open(filename)
    tkimg = ImageTk.PhotoImage(my_image)
    my_image_label.config(image=tkimg)
    my_image_label.image = tkimg  # save a reference of the image


def generate_del_tri():
    # convert PIL image to OpenCV image
    triangler_instance = triangler.Triangler()
    img = np.array(my_image.convert('RGB'))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = triangler_instance.triangulate_img(img)
    
    # convert OpenCV image back to PIL image
    img = np.asarray(img * 255.0).astype("uint8")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(img)
    # update shown image
    my_image_label.image.paste(image)


tk.Button(root, text="Load images", command=open).pack()
tk.Button(root, text="Generate triangulate", command=generate_del_tri).pack()

# for the filename of selected image
my_label = tk.Label(root)
my_label.pack()

# for showing the selected image
my_image_label = tk.Label(root)
my_image_label.pack()

root.mainloop()