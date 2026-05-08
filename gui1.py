from tkinter import*

window = Tk()

'''
window.title("윈도우 창 연습")
window.geometry("400x100")
window.resizable(width = FALSE, height = FALSE)
'''

'''
label1 = Label(window, text = "파이썬을")
label2 = Label(window, text = "열심히", font = ("궁서체", 30), fg = "blue")
label3 = Label(window, text = "공부 중입니다.", bg = "magenta", width = 20, height = 5, anchor = SE)

label1.pack()
label2.pack()
label3.pack()
'''

'''
photo1 = PhotoImage(file = "gif\puppy.gif")
label1 = Label(window, image = photo1)

photo2 = PhotoImage(file = "gif\earth.gif")
label2 = Label(window, image = photo2)

label1.pack(side = LEFT)
label2.pack()
'''

'''
button1 = Button(window, text = "파이썬 종료", fg = "red", command = quit)

button1.pack()
'''

'''
from tkinter import messagebox

def myFunc() :
    messagebox.showinfo("강아지 버튼", "강아지가 귀엽노")

photo1 = PhotoImage(file = "gif\puppy.gif")
button1 = Button(window, image = photo1, command = myFunc)

button1.pack()
'''

'''
from tkinter import messagebox

def myFunc() :
    if chk.get() == 0 :
        messagebox.showinfo("", "체크버튼이 꺼졌어요.")
    else :
        messagebox.showinfo("", "체크버튼이 켜졌어요.")

chk = IntVar()
cb1 = Checkbutton(window, text = "미세요.", variable = chk, command = myFunc)

cb1.pack()
'''

'''
def myFunc() :
    if var.get() == 1 :
        label1.configure(text = "파이썬")
    elif var.get() == 2 :
        label1.configure(text = "C++")
    else :
        label1.configure(text = "Java")

var = IntVar()
rb1 = Radiobutton(window, text = "파이썬", variable = var, value = 1, command = myFunc)
rb2 = Radiobutton(window, text = "C++", variable = var, value = 1, command = myFunc)
rb3 = Radiobutton(window, text = "Java", variable = var, value = 1, command = myFunc)

label1 = Label(window, text = "선택한 언어 :", fg = "red")

rb1.pack()
rb2.pack()
rb3.pack()
label1.pack()
'''

'''
btnList = [None]*2
fnameList = ["puppy.gif", "earth.gif"]
photoList = [None]*2
i, k = 0, 0
xPos, yPos = 0, 0
num = 0

for i in range(0,2) :
    photoList[i] = PhotoImage(file = "gif/" + fnameList[i])
    btnList[i] = Button(window, image = photoList[i])

for i in range(0,1) :
    for k in range(0,1) :
        btnList[num].place(x = xPos, y = yPos)
        num += 1
        xPos += 10

    xPos = 0
    yPos += 10
'''

from tkinter import messagebox

def clickLeft(event) :
    messagebox.showinfo("마우스", "마우스 왼쪽 버튼이 클릭됨")


window.bind("<Button-1>", clickLeft)

window.mainloop()
