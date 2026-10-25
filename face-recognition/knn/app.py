"""Tkinter front-end for the KNN face-recognition demo.

A phone-sized mock login screen that launches ``add_faces.py`` and
``recognize.py`` as subprocesses.

Run:  python app.py

Configuration (environment variables):
    FACE_APP_USERS     comma-separated list of allowed usernames
    FACE_APP_PASSWORD  demo password (default: "demo")

This is a classroom demo — it is not a real authentication system.
"""

import os
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, simpledialog

from PIL import Image, ImageTk

BASE_DIR = Path(__file__).resolve().parent
BACKGROUND_IMAGE = BASE_DIR / "s.png"
CASCADE_PATH = BASE_DIR / "data" / "haarcascade_frontalface_default.xml"


class FaceApp:
    VALID_USERNAMES = {
        name.strip().lower()
        for name in os.getenv("FACE_APP_USERS", "ali,junaidahmed,hashimashraf,aunraza").split(",")
        if name.strip()
    }
    PASSWORD = os.getenv("FACE_APP_PASSWORD", "demo")

    def __init__(self) -> None:
        self.login_window = tk.Tk()
        self.login_window.title("Login")
        self.login_window.geometry("360x640")
        self.login_background_photo = None
        self.background_photo = None

        self.create_login_frame()
        self.login_window.mainloop()

    def create_login_frame(self) -> None:
        login_frame = tk.Frame(self.login_window, bg="black", width=360, height=640)
        login_frame.pack_propagate(False)
        login_frame.pack()

        canvas = tk.Canvas(login_frame, width=360, height=640)
        canvas.pack(fill="both", expand=True)

        login_image = Image.open(BACKGROUND_IMAGE).resize((360, 640), Image.LANCZOS)
        self.login_background_photo = ImageTk.PhotoImage(login_image)
        canvas.create_image(0, 0, image=self.login_background_photo, anchor="nw")

        title = tk.Label(login_frame, text="Face App", fg="white", bg="black",
                         font=("Great Vibes", 48))
        canvas.create_window(180, 150, window=title)

        login_label = tk.Label(login_frame, text="Login", fg="white", bg="black",
                               font=("Helvetica", 18))
        canvas.create_window(180, 250, window=login_label)

        self.username_entry = tk.Entry(login_frame, font=("Helvetica", 14))
        self.username_entry.insert(0, "Username")
        self.username_entry.bind("<FocusIn>", lambda e: self.username_entry.delete(0, tk.END))
        self.username_entry.bind(
            "<FocusOut>",
            lambda e: self.username_entry.insert(0, "Username")
            if self.username_entry.get() == ""
            else None,
        )
        canvas.create_window(180, 300, window=self.username_entry)

        self.password_entry = tk.Entry(login_frame, font=("Helvetica", 14), show="*")
        self.password_entry.insert(0, "Password")
        self.password_entry.bind("<FocusIn>", lambda e: self.password_entry.delete(0, tk.END))
        self.password_entry.bind(
            "<FocusOut>",
            lambda e: self.password_entry.insert(0, "Password")
            if self.password_entry.get() == ""
            else None,
        )
        canvas.create_window(180, 350, window=self.password_entry)

        login_button = tk.Button(login_frame, text="Login", command=self.handle_login)
        canvas.create_window(180, 400, window=login_button)

    def handle_login(self) -> None:
        username = self.username_entry.get().strip().lower()
        password = self.password_entry.get()

        if username in self.VALID_USERNAMES and password == self.PASSWORD:
            self.show_main_content()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def show_main_content(self) -> None:
        self.login_window.destroy()

        self.app = tk.Tk()
        self.app.title("Face Recognition App")
        self.app.geometry("360x640")

        background_image = Image.open(BACKGROUND_IMAGE).resize((360, 640), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(background_image)

        canvas = tk.Canvas(self.app, width=360, height=640)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        add_faces_desc = tk.Label(
            self.app, text="Click here to add faces to the database",
            bg="black", fg="white", font=("Helvetica", 12),
        )
        canvas.create_window(180, 200, window=add_faces_desc)

        test_desc = tk.Label(
            self.app, text="Click here to test face recognition",
            bg="black", fg="white", font=("Helvetica", 12),
        )
        canvas.create_window(180, 330, window=test_desc)

        add_faces_button = tk.Button(self.app, text="Add Faces", command=self.run_add_faces)
        test_button = tk.Button(self.app, text="Test Faces", command=self.run_test)
        canvas.create_window(180, 250, window=add_faces_button)
        canvas.create_window(180, 370, window=test_button)

        self.app.mainloop()

    def _ensure_cascade(self) -> bool:
        if not CASCADE_PATH.exists():
            messagebox.showerror(
                "Error", "haarcascade_frontalface_default.xml not found in the 'data' directory."
            )
            return False
        return True

    def run_add_faces(self) -> None:
        if not self._ensure_cascade():
            return

        name = simpledialog.askstring("Input", "Enter your name:")
        if not name:
            messagebox.showwarning("Input Error", "Name cannot be empty. Operation cancelled.")
            return

        name = name.strip().lower()
        if name not in self.VALID_USERNAMES:
            messagebox.showwarning("Input Error", "Invalid name. Please enter one of the valid names.")
            return

        threading.Thread(
            target=lambda: subprocess.run(
                [sys.executable, "add_faces.py", name], cwd=BASE_DIR, check=False
            ),
            daemon=True,
        ).start()

    def run_test(self) -> None:
        if not self._ensure_cascade():
            return
        threading.Thread(
            target=lambda: subprocess.run(
                [sys.executable, "recognize.py"], cwd=BASE_DIR, check=False
            ),
            daemon=True,
        ).start()


if __name__ == "__main__":
    FaceApp()
