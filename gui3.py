from tkinter import*
from tkinter.filedialog import*

window = Tk()
window.geometry("400 x 100")

label1 = Label(window, text = "선택된 파일 이름")
label1.pack()

filename = askopenfilemane(parent = window, filetypes = (("GIF 파일", "*.gif"), ("모든 파일", "*.*")))

lable1.configure(text = str(filename))

window.mainloop()
