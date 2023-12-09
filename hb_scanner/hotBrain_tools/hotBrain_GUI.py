import tkinter as tk
from PIL import ImageTk, Image  # Python image loading

# Defines the structure of the custom GUI for the HotBrain backend
#TODO: Define the processes for collecting data within the GUI
class HB_GUI:
    def __init__(self, root):
        self.root = root # Set root window

        # Set background and active color palletes
        bg_Color = "#add8e6"
        ab_Color = "#add8e6"

        # Configure window
        self.root.title("HotBrain Data Collection")
        self.root.attributes('-fullscreen',True)
        self.root.configure(background=bg_Color)

        # Set up main frame and welcome label
        self.mainFrame = tk.Frame(self.root, background=bg_Color)
        self.mainFrame.pack(pady=100)
        self.welcome_Lbl = tk.Label(self.mainFrame, text="Welcome to HotBrain!", font=("Sans-Serif", 50, "bold"), 
                                    background=bg_Color)
        self.welcome_Lbl.pack()

        # Resize the logo image and place it on a canvas
        old_img = Image.open("images/HotBrainLogo.png")
        old_img = old_img.resize((600,600))
        self.img = ImageTk.PhotoImage(old_img)
        self.imgCanvas = tk.Canvas(self.mainFrame, background=bg_Color, width=600, height=600, 
                                   highlightbackground=bg_Color)
        self.imgCanvas.pack()
        self.imgCanvas.create_image(1, 1, image=self.img, anchor="nw")

        # Set up the message for user input
        self.collect_Lbl = tk.Label(self.mainFrame, text="Would you like to collect HotBrain data?", 
                                    font=("Sans-Serif", 25, "bold"), background=bg_Color)
        self.collect_Lbl.pack()

        # Create and place the buttons
        self.btnFrame = tk.Frame(self.mainFrame, background=bg_Color)
        self.btnFrame.pack(pady=10)
        self.yesbtnFrame = tk.Frame(self.btnFrame, relief="raised", borderwidth=7, background=bg_Color)
        self.yesbtnFrame.pack(padx=50, side="left")
        self.yesBtn = tk.PhotoImage(file="images/Yes_Button.png").subsample(2,2)
        self.collect_Yes_Btn = tk.Button(self.yesbtnFrame, image=self.yesBtn, borderwidth=0, 
                                         background=bg_Color, activebackground=ab_Color)
        self.collect_Yes_Btn.pack()
        self.nobtnFrame = tk.Frame(self.btnFrame, relief="raised", borderwidth=7, background=bg_Color)
        self.nobtnFrame.pack(padx=50, side='right')
        self.noBtn = tk.PhotoImage(file="images/No_Button.png").subsample(2,2)
        self.collect_No_Btn = tk.Button(self.nobtnFrame, image=self.noBtn, borderwidth=0, 
                                        background=bg_Color, activebackground=ab_Color, command=self.root.destroy)
        self.collect_No_Btn.pack()
