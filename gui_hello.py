import tkinter as tk

def say_hello() :
    label.config(text = "Hello, World!")

root = tk.Tk()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text = "Click Me", command = say_hello)
button.pack()
label = tk.Label(root, text = "No Input")
label.pack

root.mainloop()
