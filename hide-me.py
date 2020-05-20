__author__ = 'Anja Jevtovic'
__version__ = 'beta'

import tkinter as tk
from tkinter import *
from tkinter import filedialog
import PIL
from PIL import Image
import os

HEADING_FONT = ('Verdana', 40, 'bold')
WINDOW_BACKGROUND_COLOR = '#1f0033'
ACTIVE_WIDGET_COLOR = '#1f0033'
HEADING_COLOR = '#DAF7A6'
FONT_COLOR = '#DAF7A6'
STATUS_BAR_COLOR = '#e6e6ff'

image_path = ''
status_message = ''
message = ''

class Application(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.iconbitmap('C:/Users/bebe/Desktop/hide-me/Include/hide-me.ico')
        self.title('hide me')
        self.geometry("500x500")
        self.resizable(False, False)
        self.config(bg=WINDOW_BACKGROUND_COLOR)
        container = tk.Frame(self)

        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.config(width=500, height=500)

        self.frames = {}

        for F in (Start, Hide, Find):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=N+W+S+E)
            frame.config()

        self.show_frame(Start)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

class Start(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(bg=WINDOW_BACKGROUND_COLOR)
        
        hide_me_label = tk.Label(self, text='Hide me', bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR, font=HEADING_FONT)
        hide_me_label.pack(pady=60, padx=10)

        self.load_image_button = tk.Button(self, text='Load image', height=2, width=20, bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR, activebackground=ACTIVE_WIDGET_COLOR)
        self.load_image_button.bind('<Button-1>', self.load)
        self.load_image_button.pack(pady=10)

        self.load_image_label = tk.Label(self, text='', bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR)
        self.load_image_label.pack()

        self.buttons_frame = tk.Frame(self, bg=WINDOW_BACKGROUND_COLOR)
        self.buttons_frame.pack(pady=20)

        hide_button = tk.Button(self.buttons_frame, text='Hide', height=1, width=10, bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR,  command=lambda: controller.show_frame(Hide))
        hide_button.pack(side=LEFT, pady=20, padx=30, anchor=W)
        find_button = tk.Button(self.buttons_frame, text='Find', height=1, width=10, bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR,  command=lambda: controller.show_frame(Find))
        find_button.pack(side=RIGHT, pady=20, padx=30, anchor=E)

        status_bar = tk.Label(self, text='github.com/anjajevtovic @ 2020', bg=WINDOW_BACKGROUND_COLOR, fg=STATUS_BAR_COLOR)
        status_bar.pack(side=BOTTOM, fill=X, expand=True, pady=50)

    def load(self, event):
        global image_path
        get_image_path(event)
        if image_path!='' and image_path!=None:
            self.load_image_label.config(text='Selected image: ' + image_path)
        else:
            self.load_image_label.config(text='Selected image: None')
        self.load_image_button.config(activeforeground=FONT_COLOR)



class Hide(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(bg=WINDOW_BACKGROUND_COLOR)
        self.controller = controller

        back_button = tk.Button(self, text='Back', height=1, width=7, bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR)
        back_button.bind('<Button-1>', self.back)
        back_button.pack(anchor=W, pady=10)

        message_to_hide_label = tk.Label(self, text='Enter the message:', bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR)
        message_to_hide_label.pack(pady=(150,0))
        self.message_to_hide_entry = tk.Entry(self)
        self.message_to_hide_entry.pack(fill=X, pady=20)


        hide_button = tk.Button(self, text='Hide', height=1, width=10, bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR)
        hide_button.bind('<Button-1>',self.hide)
        hide_button.pack(anchor=E, pady=(10,10))

        self.status_label = tk.Label(self, text='', bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR)       
        self.status_label.pack(fill=X, anchor=W, pady=20)

        status_bar = tk.Label(self, text='github.com/anjajevtovic @ 2020', bg=WINDOW_BACKGROUND_COLOR, fg=STATUS_BAR_COLOR)
        status_bar.pack(fill=X, pady=(80,0))

    def hide(self, event):
        global image_path, status_message
        message_to_hide = self.message_to_hide_entry.get()
        self.message_to_hide_entry.delete(0, END)
        hide_message(message_to_hide)
        self.status_label.config(text=status_message)

    def back(self, event):
        self.status_label.config(text='')
        self.message_to_hide_entry.delete(0, END)
        self.controller.show_frame(Start)


class Find(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(bg=WINDOW_BACKGROUND_COLOR)

        self.controller = controller

        back_button = tk.Button(self, text='Back', height=1, width=7, bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR)
        back_button.bind('<Button-1>', self.back)
        back_button.pack(anchor=W, pady=10)

        note_label = tk.Label(self, text='Please note that only .png images can be decoded.', bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR)
        note_label.pack(pady=(10,20))

        find_button = tk.Button(self, text='Investigate', activebackground=WINDOW_BACKGROUND_COLOR, bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR)
        find_button.bind('<Button-1>',self.find)
        find_button.pack(pady=(10,20))

        self.text_frame = tk.Frame(self, bg=WINDOW_BACKGROUND_COLOR)

        self.message_text = tk.Text(self.text_frame, height=10, width=50, bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR)
        self.message_text.pack(side=LEFT, pady=10, padx=10, fill=Y)
        self.message_scroll = tk.Scrollbar(self.text_frame)
        self.message_scroll.pack(side=RIGHT, pady=10, padx=10, fill=Y)

        self.text_frame.pack()

        self.message_scroll.config(command=self.message_text.yview)
        self.message_text.config(yscrollcommand=self.message_scroll.set)

        status_bar = tk.Label(self, text='github.com/anjajevtovic @ 2020', bg=WINDOW_BACKGROUND_COLOR, fg=STATUS_BAR_COLOR)
        status_bar.pack(side=BOTTOM, fill=X, pady=(0,10))

    def find(self, event):
        global message
        find_message()
        self.message_text.insert(END, message)
    
    def back(self, event):
        self.message_text.delete(1.0, END)
        self.controller.show_frame(Start)


# UTILS
# -------------------------------------------------------------------------------------------------------

def get_image_path(event):
    global image_path
    image_path = filedialog.askopenfilename(filetypes=(('png files', '*.png'), ('jpeg files', '*.jpg')))

def text_to_binary(text):
    text_string_bits = ''.join(format(ord(text[i]), 'b').zfill(8) for i in range(len(text)))
    output = ''

    power = 0
    counter = 0
    bit = 1
    for i in range(len(text)):
        output += text_string_bits[power:power+8]
        output += str(bit)
        counter += 1
        power += 8
        if counter == len(text)-1: bit = 0

    return output

def binary_to_text(binary_text):
    power = 0
    text = ''
    for i in range(int(len(binary_text)/8)):
        c = binary_text[0+power:0+power+8]
        text += chr(int(c,2))
        power += 8
    return text

def check_capacity(width, height, text_len):
    if int((height*width*3)/9) >= text_len:
        return True
    return False

def encoding(image, text_bin, width, height):
    bit_counter = 0
    stop_signal = 0
    for x in range(width):
        if stop_signal == 0:
            for y in range(height):
                current_pixel = list(image.getpixel((x,y)))
                if(bit_counter < len(text_bin)):
                    for n in range(3):
                        current_pixel[n] = current_pixel[n] & ~1 | int(text_bin[bit_counter])
                        bit_counter += 1
                    image.putpixel((x,y), tuple(current_pixel))
                else:
                    stop_signal = 1
                    break
        else: break
    image.save(os.path.expanduser('~/Desktop/')+'hi_me.png')

def decoding(image, width, height):
    global message
    message = 'No message found!'
    retrieved_bin_data = ''

    stop_signal = 0
    bit_counter = 0

    for x in range(width):
        if stop_signal == 0:
            for y in range(height):
                current_pixel = list(image.getpixel((x,y)))
                for n in range(3):
                    if bit_counter%9 != 8:
                        retrieved_bin_data += str(current_pixel[n] & 1)
                    else:
                        if current_pixel[n] & 1 == 0: stop_signal = 1
                    bit_counter += 1
                if stop_signal == 1: break
        else: break
    message = binary_to_text(retrieved_bin_data)

# -------------------------------------------------------------------------------------------------------

def hide_message(text):
    global image_path, status_message

    if image_path != '':
        image = Image.open(image_path)
        width, height = image.size

        if check_capacity(width, height, len(text)):
            text_bin = text_to_binary(text)
            encoding(image, text_bin, width, height)
            status_message = 'Message is successfully hidden in the hi_me.png image located on your Desktop.'
        else:
            status_message = 'Err: No capacity! Message too large.'
    else:
        status_message = 'Image not selected.'
    
    
def find_message():
    global image_path, message
    if image_path != '':
        image = Image.open(image_path)
        width, height = image.size
        
        decoding(image, width, height)
    else:
        message = 'Image not selected.'



app = Application()
app.mainloop()
