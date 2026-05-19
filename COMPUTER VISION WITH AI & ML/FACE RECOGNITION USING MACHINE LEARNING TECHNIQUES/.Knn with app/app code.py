import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import threading
import subprocess
import os

class FaceApp:
    VALID_USERNAMES = {"ali", "junaidahmed", "hashimashraf", "aunraza"}
    PASSWORD = "1"

    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title("Login")
        self.login_window.geometry("360x640")  # Match size of the application window
        self.background_photo = None

        self.create_login_frame()
        self.login_window.mainloop()

    def create_login_frame(self):
        # Create and configure the login frame with a Canvas for the background image
        login_frame = tk.Frame(self.login_window, bg="black", width=360, height=640)
        login_frame.pack_propagate(False)
        login_frame.pack()

        # Create a canvas for the background image
        canvas = tk.Canvas(login_frame, width=360, height=640)
        canvas.pack(fill="both", expand=True)

        # Load and set background image for login
        login_image = Image.open("s.png")
        login_image = login_image.resize((360, 640), Image.LANCZOS)
        self.login_background_photo = ImageTk.PhotoImage(login_image)  # Preserve the reference
        canvas.create_image(0, 0, image=self.login_background_photo, anchor="nw")

        # Add title label on top of the background image
        title_label = tk.Label(login_frame, text="Face App", fg="white", bg="black", font=("Great Vibes", 48))
        canvas.create_window(180, 150, window=title_label)  # Centered at x=180, y=150

        # Add login text
        login_label = tk.Label(login_frame, text="Login", fg="white", bg="black", font=("Helvetica", 18))
        canvas.create_window(180, 250, window=login_label)  # Centered at x=180, y=250

        # Create and place the username and password fields
        self.username_entry = tk.Entry(login_frame, font=("Helvetica", 14))
        self.username_entry.insert(0, "Username")
        self.username_entry.bind("<FocusIn>", lambda e: self.username_entry.delete(0, tk.END))
        self.username_entry.bind("<FocusOut>", lambda e: self.username_entry.insert(0, "Username") if self.username_entry.get() == "" else None)
        canvas.create_window(180, 300, window=self.username_entry)  # Centered at x=180, y=300

        self.password_entry = tk.Entry(login_frame, font=("Helvetica", 14), show="*")
        self.password_entry.insert(0, "Password")
        self.password_entry.bind("<FocusIn>", lambda e: self.password_entry.delete(0, tk.END))
        self.password_entry.bind("<FocusOut>", lambda e: self.password_entry.insert(0, "Password") if self.password_entry.get() == "" else None)
        canvas.create_window(180, 350, window=self.password_entry)  # Centered at x=180, y=350

        # Create and place the login button
        login_button = tk.Button(login_frame, text="Login", command=self.handle_login)
        canvas.create_window(180, 400, window=login_button)  # Centered at x=180, y=400

    def handle_login(self):
        username = self.username_entry.get().strip().lower()
        password = self.password_entry.get()

        if username in self.VALID_USERNAMES and password == self.PASSWORD:
            self.show_main_content()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def show_main_content(self):
        # Destroy the login window
        self.login_window.destroy()

        # Create and configure the main application window
        self.app = tk.Tk()
        self.app.title("Face Recognition App")
        self.app.geometry("360x640")  # Set the window size to resemble a phone screen

        # Load and set background image
        background_image = Image.open("s.png")
        background_image = background_image.resize((360, 640), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(background_image)  # Preserve the reference

        canvas = tk.Canvas(self.app, width=360, height=640)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        # Add description labels above the buttons with more spacing
        add_faces_desc = tk.Label(self.app, text="Click here to add faces to the database", bg="black", fg="white", font=("Helvetica", 12))
        canvas.create_window(180, 200, window=add_faces_desc)  # Centered above the add_faces_button

        test_desc = tk.Label(self.app, text="Click here to test face recognition", bg="black", fg="white", font=("Helvetica", 12))
        canvas.create_window(180, 330, window=test_desc)  # Centered above the test_button

        # Create and place buttons with adjusted spacing
        add_faces_button = tk.Button(self.app, text="Add Faces", command=self.run_add_faces)
        test_button = tk.Button(self.app, text="Test Faces", command=self.run_test)

        # Create window and place buttons on the canvas with more space between them
        canvas.create_window(180, 250, window=add_faces_button)  # Positioned below the add_faces_desc
        canvas.create_window(180, 370, window=test_button)  # Positioned below the test_desc

        # Start the GUI event loop
        self.app.mainloop()

    def run_add_faces(self):
        if not os.path.exists('data/haarcascade_frontalface_default.xml'):
            messagebox.showerror("Error", "Haarcascade XML file not found in the 'data' directory.")
            return

        # Prompt user for name
        name = simpledialog.askstring("Input", "Enter your name:")
        if not name:
            messagebox.showwarning("Input Error", "Name cannot be empty. Operation cancelled.")
            return

        name = name.strip().lower()
        if name not in self.VALID_USERNAMES:
            messagebox.showwarning("Input Error", "Invalid name. Please enter one of the valid names.")
            return

        def target():
            # Pass the name as an argument to the script
            subprocess.run(['python', 'add_faces.py', name])

        thread = threading.Thread(target=target)
        thread.start()

    def run_test(self):
        if not os.path.exists('data/haarcascade_frontalface_default.xml'):
            messagebox.showerror("Error", "Haarcascade XML file not found in the 'data' directory.")
            return

        def target():
            subprocess.run(['python', 'test.py'])

        thread = threading.Thread(target=target)
        thread.start()

if __name__ == "__main__":
    FaceApp()
