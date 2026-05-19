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

# Define button click function
def button_click(button):
    if button == '=':
        try:
            result = eval(input_text.get())
            input_text.set(result)
        except:
            input_text.set('ERROR')
    elif button == 'sin':
        try:
            input_text.set(math.sin(math.radians(float(input_text.get()))))
        except:
            input_text.set('ERROR')
    elif button == 'cos':
        try:
            input_text.set(math.cos(math.radians(float(input_text.get()))))
        except:
            input_text.set('ERROR')
    elif button == 'tan':
        try:
            input_text.set(math.tan(math.radians(float(input_text.get()))))
        except:
            input_text.set('ERROR')
    else:
        current_text = input_text.get()
        new_text = current_text + button
        input_text.set(new_text)

# Create the buttons and add them to the grid individually
button_7 = tk.Button(root, text='7', width=5, command=lambda: button_click('7'))
button_7.grid(row=1, column=0, padx=5, pady=5)

button_8 = tk.Button(root, text='8', width=5, command=lambda: button_click('8'))
button_8.grid(row=1, column=1, padx=5, pady=5)

button_9 = tk.Button(root, text='9', width=5, command=lambda: button_click('9'))
button_9.grid(row=1, column=2, padx=5, pady=5)

button_sin = tk.Button(root, text='sin', width=5, command=lambda: button_click('sin'))
button_sin.grid(row=1, column=3, padx=5, pady=5)

button_4 = tk.Button(root, text='4', width=5, command=lambda: button_click('4'))
button_4.grid(row=2, column=0, padx=5, pady=5)

button_5 = tk.Button(root, text='5', width=5, command=lambda: button_click('5'))
button_5.grid(row=2, column=1, padx=5, pady=5)

button_6 = tk.Button(root, text='6', width=5, command=lambda: button_click('6'))
button_6.grid(row=2, column=2, padx=5, pady=5)

button_cos = tk.Button(root, text='cos', width=5, command=lambda: button_click('cos'))
button_cos.grid(row=2, column=3, padx=5, pady=5)

button_1 = tk.Button(root, text='1', width=5, command=lambda: button_click('1'))
button_1.grid(row=3, column=0, padx=5, pady=5)

button_2 = tk.Button(root, text='2', width=5, command=lambda: button_click('2'))
button_2.grid(row=3, column=1, padx=5, pady=5)

button_3 = tk.Button(root, text='3', width=5, command=lambda: button_click('3'))
button_3.grid(row=3, column=2, padx=5, pady=5)

button_tan = tk.Button(root, text='tan', width=5, command=lambda: button_click('tan'))
button_tan.grid(row=3, column=3, padx=5, pady=5)

button_0 = tk.Button(root, text='0', width=5, command=lambda: button_click('0'))
button_0.grid(row=4, column=0, padx=5, pady=5)

button_multiply = tk.Button(root, text='*', width=5, command=lambda: button_click('*'))
button_multiply.grid(row=4, column=1, padx=5, pady=5)

button_subtract = tk.Button(root, text='-', width=5, command=lambda: button_click('-'))
button_subtract.grid(row=4, column=2, padx=5, pady=5)

button_equal = tk.Button(root, text='=', width=5, command=lambda: button_click('='))
button_equal.grid(row=4, column=3, padx=5, pady=5)

# Handle keyboard input
def keyboard_input(event):
    if event.char in '0123456789*+-/().':
        button_click(event.char)
    elif event.keysym == 'Return':
        button_click('=')

# Bind the keyboard events to the root window
root.bind('<Key>', keyboard_input)

# Run the application
root.mainloop()
