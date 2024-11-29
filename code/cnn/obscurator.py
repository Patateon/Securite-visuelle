# Standard lib
import os
import time

# Interface lib
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory

# CNN Lib
import classifier_use

class Application(tk.Tk):

    """Basic application with tkinter"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Title
        self.title('Obscurator')

        # Resolution
        self.geometry("1050x720")
        self.resizable(0, 0)
        
        # Create a menu bar
        self.create_menu_bar()
        
        self.initialise_variables()
        
        # Initialize the main frame 
        self.scene_initializer()

    def initialise_variables(self):
        self.current_image = None
        self.current_image_path = None

    def create_menu_bar(self):
        menu_bar = tk.Menu(self)
    
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Open...", command=self.open_file)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)
        
        self.config(menu=menu_bar)


    def scene_initializer(self):
        """
        Load a main frame in the ugliest way possible.
        """

        main_frame = tk.Frame(self)


        ## Setup Image frames and controller on the left side of the window
        self.image_frame = tk.Frame(main_frame)
        
        self.image_frame_controller = tk.Frame(self.image_frame)
        
        # Add an entry and a button to the controller
        self.image_input = tk.Entry(self.image_frame_controller, width=40)
        self.image_open_button = tk.Button(self.image_frame_controller,\
            text="Open image...", command=self.open_file)
        
        # CNN Controllers
        self.input_cnn_label = tk.Label(self.image_frame_controller,\
            text="Class :")
        self.input_cnn_button = tk.Button(self.image_frame_controller,\
            text="Find class", command=self.find_input_class)
        
        self.image_input.grid(column=0, row=0)
        self.image_open_button.grid(column=1, row=0)
        
        self.input_cnn_label.grid(column=0, row=1)
        self.input_cnn_button.grid(column=1, row=1)
        
        self.image_frame_controller.pack(side="top")
        
        # Add a canvas
        self.canvas = tk.Canvas(self.image_frame, width=512, height=512, bg="blue")
    
        self.canvas.pack(side="bottom")
        
        self.image_frame.pack(side="left")
        
        ## Setup filter frame and controllers
        self.filter_frame = tk.Frame(main_frame)
        
        self.filter_controller = tk.Frame(self.filter_frame)
        
        self.filter_options = tk.StringVar(self)
        self.filter_options_names = ('BLUR', 'FREQUENCY')
        
        # Filter controllers
        self.scroller_filter = tk.OptionMenu(self.filter_controller,\
            self.filter_options, self.filter_options_names[0],\
            *self.filter_options_names)
        self.apply_filter_button = tk.Button(self.filter_controller,\
            text="Apply Filter", command=self.apply_filter)
        
        # CNN Controllers
        self.output_cnn_label = tk.Label(self.filter_controller,\
            text="Class :")
        self.output_cnn_button = tk.Button(self.filter_controller,\
            text="Find class", command=self.find_output_class)
        
        self.scroller_filter.grid(column=0, row=0)
        self.apply_filter_button.grid(column=1, row=0)
        
        self.output_cnn_label.grid(column=0, row=1)
        self.output_cnn_button.grid(column=1, row=1)
        
        self.filter_controller.pack(side="top")
        
        # Filter canvas
        self.canvas_out = tk.Canvas(self.filter_frame, width=512, height=512, bg="red")
        
        self.canvas_out.pack(side="bottom")
        
        self.filter_frame.pack(side="right")
        
        
        main_frame.pack()
        

    def display_image(self, image_path):
        self.current_image_path = image_path
        self.current_image = ImageTk.PhotoImage(Image.open(image_path))
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)

    def apply_filter(self):
        
        if self.current_image is None:
            return
        
        self.canvas_out.delete("all")
        self.canvas_out.create_image(0, 0, anchor=tk.NW, image=self.current_image)

    def find_input_class(self):
        
        if self.current_image_path is None:
            return
        
        current_image_class = classifier_use.evaluateClass(\
            classifier_use.VGG_LIKE, self.current_image_path)
        
        self.input_cnn_label['text'] = f"Class : {classifier_use.CIFAR_CLASS_NAME[current_image_class[0]]}"
        
    def find_output_class(self):
        
        if self.current_image_path is None:
            return
        
        current_image_class = classifier_use.evaluateClass(\
            classifier_use.VGG_LIKE, self.current_image_path)
        
        self.output_cnn_label['text'] = f"Class : {classifier_use.CIFAR_CLASS_NAME[current_image_class[0]]}"
        

    def open_file(self):
        """Open a file for editing."""

        path = askopenfilename(
            filetypes=[\
                ('Image Files', '.png .jpg .jpeg .ppm .mp4 .webm .mkv .avi .mov .flv .gif'),\
                ('All Files', '*.*')\
            ]
        )

        if not path:
            return
        
        if self.image_frame is not None:
            self.display_image(path)
            
        self.image_input.delete(0, 'end')
        self.image_input.insert(0, path)


    def open_dir(self):
        """Open a folder """

        path = askdirectory()

        if not path:
            return


    def save_file(self):
        """Save the current file as a new file."""

        path = asksaveasfilename(
            defaultextension='.png',
            filetypes=[\
                ('Image Files', '.png .jpg .jpeg .ppm .mp4 .webm .mkv .avi .mov .flv .gif'),\
                ('All Files', '*.*')\
            ],
        )

        if not path:
            return
     

if __name__ == "__main__":
    app = Application()
    app.mainloop()