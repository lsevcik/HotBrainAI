import tkinter as tk
from PIL import ImageTk, Image  # Python image loading

# Defines the structure of the custom GUI for the HotBrain backend
class HB_GUI:
    def __init__(self, root, sensor):
        self.root = root # Set root window
        self.sensor = sensor # Get the sensor object

        # Set background and active color palletes
        self.bg_Color = _from_rgb((0, 11, 21))
        self.ab_Color = _from_rgb((0, 11, 21))
        self.fg_Color = _from_rgb((253,0,5))
        self.yes_Color = _from_rgb((28, 94, 32))

        # Configure window
        self.root.title("HotBrain Data Collection")
        self.root.attributes('-fullscreen',True)
        self.root.configure(background=self.bg_Color)

        # Set up main frame and welcome label
        self.mainFrame = tk.Frame(self.root, background=self.bg_Color)
        self.mainFrame.pack(pady=80)
        self.welcome_Lbl = tk.Label(self.mainFrame, text="Welcome to HotBrain!", font=("Sans-Serif", 50, "bold"), 
                                    background=self.bg_Color, fg=self.fg_Color)
        self.welcome_Lbl.pack()

        # Resize the logo image and place it on a canvas
        old_img = Image.open("images/HotBrainLogo.png")
        old_img = old_img.resize((600,600))
        self.img = ImageTk.PhotoImage(old_img)
        self.imgCanvas = tk.Canvas(self.mainFrame, background=self.bg_Color, width=600, height=600, 
                                   highlightbackground=self.bg_Color)
        self.imgCanvas.pack()
        self.imgCanvas.create_image(1, 1, image=self.img, anchor="nw")

        # Set up the message for user input
        self.collect_Lbl = tk.Label(self.mainFrame, text="Would you like to collect HotBrain data?", 
                                    font=("Sans-Serif", 25, "bold"), background=self.bg_Color, fg=self.fg_Color)
        self.collect_Lbl.pack()

        # Create and place the buttons
        self.btnFrame = tk.Frame(self.mainFrame, background=self.bg_Color)
        self.btnFrame.pack(pady=20)
        self.yesbtnFrame = tk.Frame(self.btnFrame, relief="raised", borderwidth=7, background=self.yes_Color)
        self.yesbtnFrame.pack(padx=50, side="left")
        self.yesBtn = tk.PhotoImage(file="images/Yes_Button.png").subsample(3,3)
        self.collect_Yes_Btn = tk.Button(self.yesbtnFrame, image=self.yesBtn, borderwidth=0, 
                                         background=self.bg_Color, activebackground=self.ab_Color, command=self.startCollection)
        self.collect_Yes_Btn.pack()
        self.nobtnFrame = tk.Frame(self.btnFrame, relief="raised", borderwidth=7, background=self.fg_Color)
        self.nobtnFrame.pack(padx=50, side='right')
        self.noBtn = tk.PhotoImage(file="images/No_Button.png").subsample(3,3)
        self.collect_No_Btn = tk.Button(self.nobtnFrame, image=self.noBtn, borderwidth=0, 
                                        background=self.bg_Color, activebackground=self.ab_Color, command=self.root.destroy)
        self.collect_No_Btn.pack()

    # Upon clicking the checkmark (yes button) user will be prompted for input (ID)
    def startCollection(self):
        # Actual process for running with the scanner
        # from hotBrain import startUserProcess
        # startUserProcess(self.sensor)

        # Test process for running the demo, ignores scanner info (COMMENT OUT)
        from hotBrain import demo
        demo()

# Translates an rgb tuple of int to a tkinter friendly color code
# Source: Stack Overflow -> https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter
def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb  

# Initializes the user interface after scan for headband is successful
def initGUI(sensor):
    root_window = tk.Tk() # Create main window
    HB_GUI(root_window, sensor) # Create GUI
    root_window.mainloop() # Main loop
