from tkinter import *

money = 0

def earn() :
	money += 1

def money() :
    money_label.config(text = f"돈 : {earn()}")

window = Tk()
window.title("거지 키우기")
window.geometry("400x400")

label = Label(window, text = "거지 키우기", font = ("맑은 고딕", 30), fg = "blue")
label.pack(side = TOP)

money_label = Label(window, font = ("맑은 고딕", 30))
money_label.pack()

button_money = Button(window, command = earn)
button_money.pack()

window.mainloop()
