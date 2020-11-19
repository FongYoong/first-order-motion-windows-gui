import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.transform import resize
from skimage import img_as_ubyte
from demo import load_checkpoints, make_animation
import warnings
warnings.filterwarnings("ignore")

generator, kp_detector = load_checkpoints(config_path='config/vox-256.yaml', 
                                checkpoint_path='vox-cpk.pth.tar', cpu=True)

#Additions for image/video validation and display
#import imghdr
import magic
import os
from threading import Thread

def GenerateVideo():
    globs = globals()
    disable_widget_names = ["source_preview", "driving_preview", "generate_preview", 'source_button', 'driving_button', 'saveto_button']
    for widget in disable_widget_names:
        globs[widget].configure(state='disabled')
    generate_button = globs['generate_button']
    generate_button.grid_remove()
    progress_var = globs['progress_var']
    progress_bar = globs['progress_bar']
    progress_bar.grid()
    progress_label = globs['progress_label']
    progress_label.grid()

    source_address, driving_address, generated_address = globs["source_address"], globs["driving_address"], globs["generated_address"]
    #Load source image and driving video
    source_image = imageio.imread(source_address)
    reader = imageio.get_reader(driving_address)

    #Resize image and video to 256x256
    source_image = resize(source_image, (256, 256))[..., :3]

    fps = reader.get_meta_data()['fps']
    driving_video = []
    try:
        for im in reader:
            driving_video.append(im)
    except RuntimeError:
        pass
    reader.close()

    driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]

    predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True, adapt_movement_scale=True, cpu=True, progress_var=progress_var, progress_label=progress_label)
    # relative and adapt_movement_scale can be changed to obtain different results

    # Save resulting video
    imageio.mimsave(generated_address, [img_as_ubyte(frame) for frame in predictions], fps=fps)

    # View generated video
    message = messagebox.askquestion(title="Generation successfull.", message="Video at:\n" + generated_address + "\n\nView generated video?", icon="question")
    if 'yes' in message:
        os.startfile(generated_address)

    globs = globals()
    for widget in disable_widget_names:
        globs[widget].configure(state='normal')
    generate_button.grid()
    progress_var.set(0)
    progress_bar.grid_remove()
    progress_label.grid_remove()

def StartGenerateVideo():
    Thread(target=GenerateVideo, daemon=True).start() # deamon=True is important for closing the program correctly

def IsImage(image_address):
    #return True if imghdr.what(image_address) else False
    return True if "image" in magic.from_file(image_address, mime=True) else False

def IsVideo(video_address):
    return True if "video" in magic.from_file(video_address, mime=True) else False

# Additions for GUI
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import tkinter.filedialog as tkFileDialog

import webbrowser
def OpenHyperlink(url):
    webbrowser.open_new(url)

source_address = ""
driving_address = ""
generated_address = ""

def ChooseFile(variable_name, dialog_title, validation_func, failed_message, finally_func=None):
    def ChooseFileDialog():
        value = tkFileDialog.askopenfilename(title=dialog_title)
        if value:
            if not validation_func(value):
                messagebox.showerror("Error", failed_message)
                return
            exec("globals()[\"{}\"]".format(variable_name) + "= \"{}\"".format(value))
            if finally_func:
                finally_func(value)
    return ChooseFileDialog

def SaveFile(variable_name, dialog_title, finally_func=None):
    def SaveFileDialog():
        value = tkFileDialog.asksaveasfilename(title=dialog_title, initialfile="generated.mp4", defaultextension=".mp4", filetypes=(("MP4 File", "*.mp4"),("All Files", "*.*")))
        if value:
            exec("globals()[\"{}\"]".format(variable_name) + "= \"{}\"".format(value))
            if finally_func:
                finally_func()
    return SaveFileDialog

window = tk.Tk()
window.title("First-Order-Motion")
window.resizable(width=False, height=False)

#window.protocol("WM_DELETE_WINDOW", DisableCloseEvent)
#window.protocol("WM_DELETE_WINDOW", window.destroy)
#loading_label = tk.Label(window, text="Loading...")
#loading_label.pack()
#loading_label.pack_forget()

title_label = tk.Label(window, text="First-Order-Motion")
title_label.grid(row=0, column=0, padx=10, pady=10)
link1 = tk.Label(window, text="(Original Source)", fg="blue", cursor="hand2")
link1.bind("<Button-1>", lambda e: OpenHyperlink("https://aliaksandrsiarohin.github.io/first-order-model-website/"))
link1.grid(row=0, column=1, padx=10, pady=10)
link2 = tk.Label(window, text="(Github)", fg="blue", cursor="hand2")
link2.bind("<Button-1>", lambda e: OpenHyperlink("https://github.com/FongYoong/first-order-motion-windows-gui"))
link2.grid(row=0, column=2, padx=10, pady=10)

def GetFileName(address):
    #address.encode('unicode_escape')
    return os.path.basename(address)

source_preview, driving_preview, generate_preview = None, None, None

def PreviewImage(image_address):
    #source_name = tk.Label(master=window, text=GetFileName(image_address), borderwidth=2, relief="groove")
    #source_name.configure(font="Verdana 12 underline")
    #source_name.grid(row=1, column=2, padx=5, pady=10)
    source_preview = globals()["source_preview"]
    if source_preview:
        source_preview.grid_remove()
    source_preview = tk.Button(master=window, text=GetFileName(image_address), command= lambda _ = None: os.startfile(image_address))
    source_preview.grid(row=1, column=2, padx=5, pady=10)
    globals()["source_preview"] = source_preview
    ShowGenerateButton()

def PreviewVideo(video_address):
    driving_preview = globals()["driving_preview"]
    if driving_preview:
        driving_preview.grid_remove()
    driving_preview = tk.Button(master=window, text=GetFileName(video_address), command= lambda _ = None: os.startfile(video_address))
    driving_preview.grid(row=2, column=2, padx=5, pady=10)
    globals()["driving_preview"] = driving_preview
    ShowGenerateButton()

def ShowGenerateButton():
    source_address, driving_address, generated_address = globals()["source_address"], globals()["driving_address"], globals()["generated_address"]
    if generated_address:
        generate_preview = globals()["generate_preview"]
        if generate_preview:
            generate_preview.grid_remove()
        file_name = GetFileName(generated_address)
        generate_preview = tk.Button(master=window, text=file_name, command= lambda _ = None: os.startfile(generated_address.replace(str(file_name), "")))
        generate_preview.grid(row=3, column=2, padx=5, pady=10)
        globals()["generate_preview"] = generate_preview
        generate_button = globals()["generate_button"]
        if source_address and driving_address:
            #ttk.Separator(master=window, orient=tk.HORIZONTAL).grid(row=4, column=0, columnspan=3, sticky='W')
            generate_button.grid()
        else:
            generate_button.grid_remove()
    
source_label = tk.Label(master=window, text="Source Image")
source_label.grid(row=1, column=0, pady=10)
source_button = tk.Button(master=window, text="Select File", command=ChooseFile("source_address", "Select Source Image", IsImage, "Invalid Image", finally_func=PreviewImage))
source_button.grid(row=1, column=1, pady=10)
driving_label = tk.Label(master=window, text="Driving Video")
driving_label.grid(row=2, column=0, pady=10)
driving_button = tk.Button(master=window, text="Select File", command=ChooseFile("driving_address", "Select Driving Video", IsVideo, "Invalid Video", finally_func=PreviewVideo))
driving_button.grid(row=2, column=1, pady=10)
saveto_label = tk.Label(master=window, text="Save Location")
saveto_label.grid(row=3, column=0, pady=10)
saveto_button = tk.Button(master=window, text="Save As", command=SaveFile("generated_address", "Select Folder", finally_func=ShowGenerateButton))
saveto_button.grid(row=3, column=1, pady=10)
generate_button = tk.Button(master=window, text="Generate Animation", fg="green", command=StartGenerateVideo)
generate_button.grid(row=5, column=1, pady=10)
generate_button.grid_remove()
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(master=window, orient="horizontal", mode="determinate", variable=progress_var, maximum=100)
progress_bar.grid(row=5, column=0, pady=5, padx=5, sticky=tk.E+tk.W+tk.N+tk.S, columnspan=3)
progress_bar.grid_remove()
progress_label = tk.Label(master=window, text="0 %")
progress_label.grid(row=6, column=1, pady=10)
progress_label.grid_remove()
window.mainloop()