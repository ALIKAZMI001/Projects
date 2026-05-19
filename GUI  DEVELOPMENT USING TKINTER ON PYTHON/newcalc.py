import tkinter as tk
import math

# Create the main application window
root = tk.Tk()

# Set the window title
root.title("Calculator")

# Change the icon
icon = tk.PhotoImage(file='calc.png')
root.iconphoto(False, icon)

# Create the input field
input_text = tk.StringVar()
input_field = tk.Entry(root, textvariable=input_text, justify='right', width=30)
input_field.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

# Initialize memory
memory = 0

# Create the buttons
buttons = [
    '7', '8', '9', '/', 'sin',
    '4', '5', '6', '*', 'cos',
    '1', '2', '3', '-', 'tan',
    '0', '.', '=', '+', 'sqrt',
]

# Define button click function
def button_click(button):
    if button == '=':
        try:
            result = eval(input_text.get())
            input_text.set(result)
            history_text.insert(tk.END, input_text.get() + '\n')
        except:
            input_text.set('ERROR')
    elif button == 'C':
        clear_input()
    elif button == 'DEL':
        delete_char()
    elif button == 'sin':
        input_text.set(math.sin(math.radians(float(input_text.get()))))
    elif button == 'cos':
        input_text.set(math.cos(math.radians(float(input_text.get()))))
    elif button == 'tan':
        input_text.set(math.tan(math.radians(float(input_text.get()))))
    elif button == 'sqrt':
        input_text.set(math.sqrt(float(input_text.get())))
    else:
        current_text = input_text.get()
        new_text = current_text + button
        input_text.set(new_text)

# Create the buttons and add them to the grid
row = 1
col = 0
for button in buttons:
    button_action = lambda x=button: button_click(x)
    tk.Button(root, text=button, width=5, command=button_action).grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col > 4:
        col = 0
        row += 1

# Add memory functions
def memory_add():
    global memory
    current_input = input_text.get()
    try:
        current_input = float(current_input)
        memory += current_input
    except:
        pass

def memory_subtract():
    global memory
    current_input = input_text.get()
    try:
        current_input = float(current_input)
        memory -= current_input
    except:
        pass

def memory_recall():
    global memory
    input_text.set(str(memory))

def memory_clear():
    global memory
    memory = 0

# Add memory buttons
tk.Button(root, text='M+', width=5, command=memory_add).grid(row=5, column=0, padx=5, pady=5)
tk.Button(root, text='M-', width=5, command=memory_subtract).grid(row=5, column=1, padx=5, pady=5)
tk.Button(root, text='MR', width=5, command=memory_recall).grid(row=5, column=2, padx=5, pady=5)
tk.Button(root, text='MC', width=5, command=memory_clear).grid(row=5, column=3, padx=5, pady=5)

# Define clear input function
def clear_input():
    input_text.set('')

# Define delete character function
def delete_char():
    current_text = input_text.get()
    new_text = current_text[:-1]
    input_text.set(new_text)

# Add clear and delete buttons
clear_button = tk.Button(root, text='C', width=5, command=clear_input)
clear_button.grid(row=6, column=0, padx=5, pady=5)
delete_button = tk.Button(root, text='DEL', width=5, command=delete_char)
delete_button.grid(row=6, column=1, padx=5, pady=5)

# Add history log
history_text = tk.Text(root, width=25, height=5)
history_text.grid(row=1, column=5, rowspan=5, padx=5, pady=5)

# Handle keyboard input
def keyboard_input(event):
    if event.char in '0123456789+-*/.()':
        button_click(event.char)
    elif event.keysym == 'Return':
        button_click('=')
    elif event.keysym == 'BackSpace':
        delete_char()

# Bind the keyboard events to the root window
root.bind('<Key>', keyboard_input)

# Run the application
root.mainloop()
