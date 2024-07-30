import tkinter as tk
import customtkinter as ctk
import random
import threading
from datetime import datetime, timedelta
import time
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import cv2
import winsound

class PhoneNumberEntry(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        self.text_var = tk.StringVar()
        super().__init__(master, textvariable=self.text_var, **kwargs)
        self.bind("<FocusOut>", self.format_phone_number)
        self.bind("<Return>", self.format_phone_number)
        self.bind("<Return>", self.on_enter_pressed)
        self.bind("<KeyPress-e>", self.on_e_pressed)  # Bind 'e' key for frame switching
        self.configure(validate="key", validatecommand=(self.register(self.validate_input), "%P"))

    def validate_input(self, new_value):
        # Only allow numeric input
        return new_value == "" or new_value.isdigit()

    def format_phone_number(self, event=None):
        # Get the current text
        text = self.text_var.get()

        # Remove all non-numeric characters
        digits = ''.join(filter(str.isdigit, text))

        # Limit to 10 digits for a standard phone number
        if len(digits) > 10:
            digits = digits[:10]

        # Format the text with dashes and parentheses
        formatted_text = ''
        if len(digits) > 0:
            formatted_text += '(' + digits[:3] + ')'
        if len(digits) > 3:
            formatted_text += ' ' + digits[3:6]
        if len(digits) > 6:
            formatted_text += '-' + digits[6:10]

        # Update the text variable
        self.text_var.set(formatted_text)

    def on_enter_pressed(self, event=None):
        # Disable further input
        self.configure(state='disabled')

    def on_e_pressed(self, event=None):
        # Call the method to switch back to frame 0
        app.switch_frame(0)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("1080x720")

        # Create a list to store the frames
        self.frames = [ctk.CTkFrame(master=self) for _ in range(21)]  # 20 frames + 1 for index 0

        # Pack all frames
        for frame in self.frames:
            frame.pack(fill='both', expand=True)

        # Initially, only show the first frame
        for frame in self.frames[1:]:
            frame.pack_forget()

        # Create the phone number entry widget (just for demonstration; remove if not needed)
        label = ctk.CTkLabel(master=self.frames[1], text="Please enter your phone number \n Press Enter to format \n Press E to call", font=("TkDefaultFont", 30, "bold"))
        label.grid(row=0, column=100, padx=300, pady=30)

        self.phone_entry = PhoneNumberEntry(master=self.frames[1], font=("TkDefaultFont", 45, "bold"), width=400, height=50)
        self.phone_entry.grid(row=1, column=100, padx=300, pady=5)
        self.current_frame_index = 0

        # Create the home buttons in the first frame
        self.create_home_page1(self.frames[0])

        # Define key bindings for frames
        self.key_frame_map = {
            '1': 1,     # Switch to frame 1
            '2': 2,     # Switch to frame 2
            '3': 3,     # Switch to frame 3
            '4': 4,     # Switch to frame 4
            '5': 5,     # Switch to frame 5
            '6': 6,     # Switch to frame 6
            '7': 7,     # Switch to frame 7
            '8': 8,     # Switch to frame 8
            '9': 9,     # Switch to frame 9
            '10': 10,    # Switch to frame 10
            '11': 11,    # Switch to frame 11
            '12': 12     # Switch to frame 12
        }

        # Bind keys to frame switching
        for key in self.key_frame_map:
            if int(key) <= 8:
                self.bind(f"<Control-Key-{key}>", lambda event, k=key: self.handle_key_press(event, 1))
            else:
                new_key = str(int(key) - 8)
                self.bind(f"<Alt-Key-{new_key}>", lambda event, k=new_key: self.handle_key_press(event, 2))

        # Bind the Esc key to switch to frame 0
        self.bind("<Escape>", self.switch_to_frame_0)

        # Initialize the second home page on the 20th frame
        self.create_home_page2(self.frames[20])

        # Set up the camera in frame 2
        self.setup_camera_frame(self.frames[2])

        # Setup the weather info frame
        self.setup_weather_frame(self.frames[3])

        # setup contacts frame
        self.setup_contacts_frame(self.frames[4])

        self.setup_schedule_frame(self.frames[5])

        self.setup_bus_schedule_frame(self.frames[6])

        self.setup_random_word_frame(self.frames[7])

        self.setup_color_change_frame(self.frames[8])

        self.setup_notepad_frame(self.frames[9])

        self.setup_alarm_clock_frame(self.frames[10])

        self.setup_stopwatch_frame(self.frames[11])

    def create_home_page1(self, frame):
        # Button texts for the first home page
        button_texts = [
            "📱\n Cellphone \n Press Ctrl 1", "📷\n Camera \n Press Ctrl 2", " ☀️\n Weather \n Press Ctrl 3", "📇\n Contacts \n Press Ctrl 4",
            "📅\n Class Schedule \n Press Ctrl 5", "🚌\n Bus Schedule \n Press Ctrl 6", "🎲\n Word Randomizer \n Press Ctrl 7", "⚙️\n Settings \n Press Ctrl 8",
            "📝\n Notepad \n Press Shift 1", "item, Press shift 2", "item shift 3", "item Press Shift 4"
        ]

        # Create and place buttons in the grid
        for idx, text in enumerate(button_texts):
            row = idx // 4  # Determine the row number (0, 1)
            col = idx % 4   # Determine the column number (0, 1, 2, 3)
            button = ctk.CTkButton(master=frame, text=text, fg_color="grey", width=130, height=70, command=lambda r=row, c=col: self.on_home_button_click(r, c), font=("TkDefaultFont", 27, "bold"), hover_color='grey')
            button.grid(row=row, column=col, padx=8, pady=10, sticky='nsew')

        # Add the button to navigate to the second home page
        nav_button = ctk.CTkButton(master=frame, text="More Options", fg_color="grey", width=130, height=70, command=lambda: self.switch_frame(20), font=("TkDefaultFont", 30, "bold"), hover_color='grey')
        nav_button.grid(row=2, column=0, columnspan=4, padx=8, pady=10, sticky='nsew')

        # Configure grid row and column weights
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)  # Row for the navigation button
        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)

    def create_home_page2(self, frame):
        # Button texts for the second home page
        button_texts = [
            "📝\n Notepad \n Press Alt 1", "⏰\n Alarm \n Press Alt 2", "⏱️\n Stopwatch \n Alt 3", "-", "-", "-", "-", "-" 
        ]

        # Create and place buttons in the grid
        for idx, text in enumerate(button_texts):
            row = idx // 4  # Determine the row number (0, 1)
            col = idx % 4   # Determine the column number (0, 1, 2, 3)
            button = ctk.CTkButton(master=frame, text=text, fg_color="grey", width=130, height=70, command=lambda r=row, c=col: self.on_home_button_click(r, c+8), font=("TkDefaultFont", 30, "bold"), hover_color='grey')
            button.grid(row=row, column=col, padx=8, pady=10, sticky='nsew')

        # Add the button to navigate back to the first home page
        back_button = ctk.CTkButton(master=frame, text="Back to Main Menu", fg_color="grey", width=130, height=70, command=lambda: self.switch_frame(0), font=("TkDefaultFont", 30, "bold"), hover_color='grey')
        back_button.grid(row=2, column=0, columnspan=4, padx=8, pady=10, sticky='nsew')

        # Configure grid row and column weights
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)  # Row for the back button
        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)

    def switch_to_frame_0(self, event):
        self.switch_frame(0)


    def setup_camera_frame(self, frame):
        self.cap = cv2.VideoCapture(0)  # Try to open the default camera
        self.camera_label = ctk.CTkLabel(master=frame, text="")
        self.camera_label.pack(fill='both', expand=True)

        if not self.cap.isOpened():
            self.camera_label.configure(text="No camera available")
        else:
            self.update_camera_feed()

    def update_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)
        self.camera_label.after(10, self.update_camera_feed)

    def setup_weather_frame(self, frame):
        try:
            with open('G:\My Drive\COSC 111\weather_info.txt', 'r') as file:
                weather_info = file.read()
        except FileNotFoundError:
            weather_info = "Weather information not available."

        self.weather_label = ctk.CTkLabel(master=frame, text=weather_info, font=("TkDefaultFont", 50, "bold"))
        self.weather_label.pack(padx=20, pady=20)

    def setup_contacts_frame(self, frame):
        try:
            with open('G:\My Drive\COSC 111\contacts.txt', 'r') as file:
                contacts_info = file.read()
        except FileNotFoundError:
            contacts_info = "contacts information not available."

        self.contactlabel = ctk.CTkLabel(master=frame, text=contacts_info, font=("TkDefaultFont", 50, "bold"))
        self.contactlabel.pack(padx=20, pady=20)

        # Add a button to prompt for name and number and update the label
        self.add_info_button = ctk.CTkButton(master=frame, text="Add Info", command=self.prompt_for_info, font=("TkDefaultFont", 20, "bold"))
        self.add_info_button.pack(padx=20, pady=20)

    def prompt_for_info(self):
        # Prompt for name
        name = simpledialog.askstring("Input", "Enter name:")
        if name is None:
            return  # User canceled the input

        # Prompt for number
        number = simpledialog.askstring("Input", "Enter number:")
        if number is None:
            return  # User canceled the input

        # Update the label with the new information
        current_text = self.contactlabel.cget("text")
        new_info = f"{current_text}\n{name}: {number}"
        self.contactlabel.configure(text=new_info)

    def setup_schedule_frame(self, frame):
        # Read the schedule data from the file
        try:
            with open('G:/My Drive/COSC 111/UFV_schedule.txt', 'r') as file:
                schedule_info = file.read()
        except FileNotFoundError:
            schedule_info = "Schedule information not available."

        self.weather_label = ctk.CTkLabel(master=frame, text=schedule_info, font=("TkDefaultFont", 50, "bold"))
        self.weather_label.pack(padx=20, pady=20)
        
    def setup_bus_schedule_frame(self, frame):
        # Implementation for bus schedule frame
        try:
            with open(r'G:\My Drive\COSC 111\bus_schedule.txt', 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            lines = [
                "Vancouver to UFV Abbotsford, 1pm",
                "Vancouver to UFV Abbotsford, 2pm",
                "UFV Chilliwack to UFV Abbotsford, 2pm",
                "UFV Chilliwack to UFV Abbotsford, 3pm",
                "UFV Chilliwack to UFV Abbotsford, 4pm"
            ]

        header = ["Route", "Time"]

        # Create labels for the header
        for col, text in enumerate(header):
            label = ctk.CTkLabel(master=frame, text=text, font=("TkDefaultFont", 50, "bold"))
            label.grid(row=0, column=col, padx=10, pady=5, sticky='nsew')

        # Create labels for the schedule rows
        for row, line in enumerate(lines, start=1):
            columns = line.strip().split(", ")
            for col, text in enumerate(columns):
                label = ctk.CTkLabel(master=frame, text=text, font=("TkDefaultFont", 35), bg_color='grey')
                label.grid(row=row, column=col, padx=10, pady=5, sticky='nsew')

        # Configure row and column weights to ensure proper resizing
        for col in range(len(header)):
            frame.grid_columnconfigure(col, weight=1)
        for row in range(len(lines) + 1):
            frame.grid_rowconfigure(row, weight=1)

    
    def setup_random_word_frame(self, frame):
        # Read the list of random words from the file
        try:
            with open("G:\My Drive\COSC 111\wrandom_words.txt", 'r') as file:
                words = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            words = ["apple", "banana", "cherry", "date", "elderberry"]

        # Create a label to display the random word
        self.random_word_label = ctk.CTkLabel(master=frame, text="", font=("TkDefaultFont", 60, "bold"))
        self.random_word_label.pack(pady=60)

        # Function to display a random word
        def display_random_word():
            random_word = random.choice(words)
            self.random_word_label.configure(text=random_word)

        # Create a button to generate and display a random word
        random_word_button = ctk.CTkButton(master=frame, text="Show Random Word", command=display_random_word, font=("TkDefaultFont", 80, "bold"), fg_color='grey')
        random_word_button.pack(pady=40)

        # Configure frame to ensure proper resizing
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def setup_color_change_frame(self, frame):
        # Label to prompt user to choose a background color
        label = ctk.CTkLabel(master=frame, text="Choose Background Color", font=("TkDefaultFont", 24, "bold"))
        label.pack(pady=20)

        # Colors to choose from
        colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "gray"]

        def change_color(color):
            # Change the background color of all frames
            for f in self.frames:
                f.configure(fg_color=color)  # Change background color of each frame
            self.configure(fg_color=color)  # Optionally change the background color of the window

        # Create color buttons
        for color in colors:
            button = ctk.CTkButton(master=frame, text=color.capitalize(), command=lambda c=color: change_color(c), font=("TkDefaultFont", 20, "bold"), fg_color=color)
            button.pack(side='left', padx=10, pady=10)

        # Configure frame to ensure proper resizing
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)


    def setup_notepad_frame(self, frame):
        # Add a label
        label = ctk.CTkLabel(master=frame, text="Simple Notepad", font=("TkDefaultFont", 40, "bold"))
        label.pack(pady=20)

        # Create a frame with rounded corners for the text area
        rounded_frame = ctk.CTkFrame(master=frame, corner_radius=15)
        rounded_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Text area for notes inside the rounded frame
        text_area = tk.Text(master=rounded_frame, wrap="word", font=("TkDefaultFont", 25), bd=0)
        text_area.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Match the Text widget background color to the rounded frame color
        text_area.configure(bg="white")

        # Save notes to a file
        def save_notes():
            with open("notes.txt", "w") as file:
                file.write(text_area.get(1.0, tk.END))

        # Load notes from a file
        def load_notes():
            try:
                with open("notes.txt", "r") as file:
                    content = file.read()
                    text_area.delete(1.0, tk.END)
                    text_area.insert(tk.END, content)
            except FileNotFoundError:
                pass  # No previous notes saved

        # Save button
        save_button = ctk.CTkButton(master=frame, text="Save", command=save_notes, font=("TkDefaultFont", 30, "bold"), fg_color='grey')
        save_button.pack(pady=0)

        # Load button
        load_button = ctk.CTkButton(master=frame, text="Load", command=load_notes, font=("TkDefaultFont", 30, "bold"), fg_color='grey')
        load_button.pack(pady=10)


    def setup_alarm_clock_frame(self, frame):
        self.alarm_time = None
        self.alarm_thread = None
        self.is_alarm_active = False

        # Create and place widgets
        self.alarm_label = ctk.CTkLabel(master=frame, text="Set Alarm (HH:MM:SS)", font=("TkDefaultFont", 20, "bold"))
        self.alarm_label.pack(pady=10)

        self.alarm_entry = ctk.CTkEntry(master=frame, font=("TkDefaultFont", 20), width=200)
        self.alarm_entry.pack(pady=5)

        self.set_alarm_button = ctk.CTkButton(master=frame, text="Set Alarm", command=self.set_alarm, font=("TkDefaultFont", 20))
        self.set_alarm_button.pack(pady=10)

        self.current_time_label = ctk.CTkLabel(master=frame, text="", font=("TkDefaultFont", 30, "bold"))
        self.current_time_label.pack(pady=10)

        self.update_clock()

    def set_alarm(self):
        alarm_str = self.alarm_entry.get()
        try:
            # Parse the alarm time from the input
            alarm_time = datetime.strptime(alarm_str, "%H:%M:%S").time()
            now = datetime.now()
            alarm_datetime = datetime.combine(now.date(), alarm_time)
            
            # If the alarm time is earlier than current time, set for the next day
            if alarm_datetime <= now:
                alarm_datetime += timedelta(days=1)
            
            # Calculate the sleep duration
            self.alarm_duration = (alarm_datetime - now).total_seconds()
            print(f"Current Time: {now}")
            print(f"Alarm Time: {alarm_datetime}")
            print(f"Duration: {self.alarm_duration} seconds")

            self.is_alarm_active = True
            if self.alarm_thread and self.alarm_thread.is_alive():
                self.alarm_thread.join()  # Ensure previous thread is stopped
            self.alarm_thread = threading.Thread(target=self.check_alarm)
            self.alarm_thread.start()
            messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter time in HH:MM:SS format")

    def check_alarm(self):
        if self.alarm_duration > 0:
            print(self.alarm_duration)
            time.sleep(self.alarm_duration)
            self.alarm()
        self.is_alarm_active = False

    def alarm(self):
        # Play sound (Windows only). For cross-platform, consider libraries like `playsound`.
        winsound.Beep(1000, 5000)  # Frequency 1000 Hz, Duration 5000 ms
        messagebox.showinfo("Alarm", "Time's up!")

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.current_time_label.configure(text=now)
        self.after(1000, self.update_clock)  # Update every second

    def setup_stopwatch_frame(self, frame):
        self.stopwatch_start_time = None
        self.stopwatch_elapsed_time = 0
        self.stopwatch_thread = None
        self.is_stopwatch_running = False

        # Create and place widgets
        self.stopwatch_label = ctk.CTkLabel(master=frame, text="Stopwatch", font=("TkDefaultFont", 40, "bold"))
        self.stopwatch_label.pack(pady=10)

        self.stopwatch_display = ctk.CTkLabel(master=frame, text="00:00:00", font=("TkDefaultFont", 100))
        self.stopwatch_display.pack(pady=20)

        # Create a frame to contain the buttons and pack it centrally
        button_frame = ctk.CTkFrame(master=frame, corner_radius=10, fg_color=frame.cget('fg_color'))
        button_frame.pack(pady=10, fill='x', expand=True)

        # Add buttons to the button frame
        self.start_button = ctk.CTkButton(master=button_frame, text="Start", command=self.start_stopwatch, font=("TkDefaultFont", 60), fg_color='grey')
        self.start_button.pack(side="left", padx=10, expand=True)

        self.stop_button = ctk.CTkButton(master=button_frame, text="Stop", command=self.stop_stopwatch, font=("TkDefaultFont", 60), fg_color='grey')
        self.stop_button.pack(side="left", padx=10, expand=True)

        self.reset_button = ctk.CTkButton(master=button_frame, text="Reset", command=self.reset_stopwatch, font=("TkDefaultFont", 60), fg_color='grey')
        self.reset_button.pack(side="left", padx=10, expand=True)

        

    def start_stopwatch(self):
        if not self.is_stopwatch_running:
            self.stopwatch_start_time = time.time() - self.stopwatch_elapsed_time
            self.is_stopwatch_running = True
            if self.stopwatch_thread and self.stopwatch_thread.is_alive():
                self.stopwatch_thread.join()
            self.stopwatch_thread = threading.Thread(target=self.update_stopwatch)
            self.stopwatch_thread.start()

    def stop_stopwatch(self):
        if self.is_stopwatch_running:
            self.is_stopwatch_running = False
            if self.stopwatch_thread:
                self.stopwatch_thread.join()

    def reset_stopwatch(self):
        if self.is_stopwatch_running:
            self.is_stopwatch_running = False
            if self.stopwatch_thread:
                self.stopwatch_thread.join()
        self.stopwatch_elapsed_time = 0
        self.stopwatch_start_time = None
        self.update_stopwatch_display()

    def update_stopwatch(self):
        while self.is_stopwatch_running:
            self.stopwatch_elapsed_time = time.time() - self.stopwatch_start_time
            self.update_stopwatch_display()
            time.sleep(0.1)  # Update every 100 milliseconds

    def update_stopwatch_display(self):
        elapsed = timedelta(seconds=self.stopwatch_elapsed_time)
        hours, remainder = divmod(elapsed.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.stopwatch_display.configure(text=time_str)

    def on_home_button_click(self, row, col):
        # Determine the frame index based on row and column
        frame_index = row * 4 + col + 1
        if frame_index > 0 and frame_index < len(self.frames):
            self.switch_frame(frame_index)

    def Create_Back_Button(self, frame, next_frame):
        def go_back():
            self.switch_frame(self.frames.index(next_frame))

        # Create the back button
        back_button = ctk.CTkButton(master=frame, text="Home", fg_color="grey", width=130, height=70, command=go_back, font=("TkDefaultFont", 30, "bold"), hover_color='grey')

        # Place the button in the frame with specific coordinates
        back_button.place(x=10, y=10)  # Adjust x and y as needed for positioning

        # Optionally, you can use `anchor` to control the alignment if needed
        # back_button.place(x=10, y=10, anchor='nw')





    def switch_frame(self, next_frame_index):
        if 0 <= next_frame_index < len(self.frames):
            self.frames[self.current_frame_index].pack_forget()
            self.frames[next_frame_index].pack(fill='both', expand=True)
            self.current_frame_index = next_frame_index  # Update the current frame index

    def handle_key_press(self, event, page):
        # Check if the key pressed is in the key_frame_map dictionary
        if event.keysym in self.key_frame_map:
            if page == 1:
                type(event.keysym)
                self.switch_frame(self.key_frame_map[event.keysym])
            if page == 2:
                new_event_keysym = str(int(event.keysym) + 8)
                self.switch_frame(self.key_frame_map[new_event_keysym])

    def go_back_from_frame(self):
        # Determine the previous frame index
        prev_index = self.current_frame_index - 1
        if prev_index < 0:
            prev_index = 0  # Ensure we don't go before the first frame

        # Switch back to the previous frame
        self.switch_frame(prev_index)

app = App()

# Create back buttons for frames 1 through 19 (excluding frame 20)
for i in range(1, 20):
    app.Create_Back_Button(app.frames[i], app.frames[0])

# Setup color change frame (Frame 7)



app.mainloop()
