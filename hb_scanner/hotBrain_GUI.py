import tkinter as tk
from PIL import ImageTk, Image  # Python image loading

# Translates rgb values into tkinter color code
def rgbToColor(rgb):
    return "#%02x%02x%02x" % rgb  

# Set color palletes
bg_Color = rgbToColor((0, 11, 21))
fg_Color = rgbToColor((253,0,5))
yes_Color = rgbToColor((28, 94, 32))

# Defines the structure of the custom GUI for the HotBrain backend
class HB_GUI:
    def __init__(self, root, sensor):
        self.root = root # Set root window
        self.sensor = sensor # Get the sensor object

        # Configure window
        self.root.title("HotBrain Data Collection")
        self.root.attributes('-fullscreen',True)
        self.root.configure(background=bg_Color)

        # Set up main frame and welcome label
        self.mainFrame = tk.Frame(self.root, background=bg_Color)
        self.mainFrame.pack(pady=80)
        self.welcome_Lbl = tk.Label(self.mainFrame, text="Welcome to HotBrain!", font=("Sans-Serif", 50, "bold"), 
                                    background=bg_Color, fg=fg_Color)
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
                                    font=("Sans-Serif", 25, "bold"), background=bg_Color, fg=fg_Color)
        self.collect_Lbl.pack()

        # Create and place the buttons
        self.btnFrame = tk.Frame(self.mainFrame, background=bg_Color)
        self.btnFrame.pack(pady=20)
        self.yesbtnFrame = tk.Frame(self.btnFrame, relief="raised", borderwidth=7, background=yes_Color)
        self.yesbtnFrame.pack(padx=50, side="left")
        self.yesBtn = tk.PhotoImage(file="images/Yes_Button.png").subsample(3,3)
        self.collect_Yes_Btn = tk.Button(self.yesbtnFrame, image=self.yesBtn, borderwidth=0, 
                                         background=bg_Color, activebackground=bg_Color, command=self.startCollection)
        self.collect_Yes_Btn.pack()
        self.nobtnFrame = tk.Frame(self.btnFrame, relief="raised", borderwidth=7, background=fg_Color)
        self.nobtnFrame.pack(padx=50, side='right')
        self.noBtn = tk.PhotoImage(file="images/No_Button.png").subsample(3,3)
        self.collect_No_Btn = tk.Button(self.nobtnFrame, image=self.noBtn, borderwidth=0, 
                                        background=bg_Color, activebackground=bg_Color, command=self.root.destroy)
        self.collect_No_Btn.pack()

    # Creates the pop up window and returns the user input
    def createTokenPopUp(self):
        return TokenPopUp(self.root).awaitInput()

    # Upon clicking the checkmark (yes button) user will be prompted for input (ID)
    def startCollection(self):
        # Actual process for running with the scanner
        # from hotBrain import startUserProcess
        # startUserProcess(self, self.sensor)

        # Test process for running the demo, ignores scanner info (COMMENT OUT)
        from hotBrain import demo
        demo(self)

# Creates a pop up window for the user to enter their token (user id)
class TokenPopUp():
    def __init__(self, root):
        # Configure window
        self.top = tk.Toplevel(root, background=bg_Color)
        width, height = 600, 75
        self.top.geometry(f"{width}x{height}")
        self.top.resizable(0, 0) # Set window as fixed
        self.top.wm_transient(root) # Set this window as always on top of root

        # Center window on screen
        x = root.winfo_screenwidth()
        y = root.winfo_screenheight()
        win_x = int((x/2) - (width/2))
        win_y = int((y/2) - (height/2))
        self.top.geometry(f'+{win_x}+{win_y}')

        # Create window text and entry box
        self.token_Lbl = tk.Label(self.top, text="Please enter your token below (Or scan from the QR code)",
                                    font=("Sans-Serif", 15, "bold"), background=bg_Color, fg=fg_Color)
        self.token_Lbl.pack()
        self.tokenInput = tk.Entry(self.top, width=25, background=bg_Color, fg=fg_Color, 
                                    insertbackground=fg_Color, borderwidth=5, relief="groove")
        self.tokenInput.pack()

        self.top.grab_set() # Disable root window from user interaction

    # Window will wait until some text is entered into the entry box
    def awaitInput(self):
        token = None

        # Checks user input for text, destroys window if not empty
        def callback(event):
            nonlocal token
            token = self.tokenInput.get()
            if token != "":
                self.top.destroy()

        self.tokenInput.bind("<Return>", callback) # Binds the enter key to the entry box for input
        self.top.wait_window() # Waits until the token variable is modified
        return token

# Initializes the user interface after scan for headband is successful
def initGUI(sensor):
    root_window = tk.Tk() # Create main window
    HB_GUI(root_window, sensor) # Create GUI
    root_window.mainloop() # Main loop
