from tkinter import *

def sword :
    def __init__(self, level = 1, money = 10000) :
        self.level = level
        self.money = money

    def reinforce(self) :
        #검 강화(확률 = 95, 90, 80, 70, 50, 30, 10, 1 퍼센트 / 총 10강)
        #강화 비용(판매 가격의 10분의 1)
        self.level += 1
        self.money -=

    def sell(self) :
        #검 판매(가격 = 1, 2, 4, 8, 16, 32, 64, 128, 256, 1000 단위:천)
        self.level = 0
        self.money -= 









window = Tk()
window.title("앱 모음")
window.geometry("360x150")

label = Label(window, text = "")




winidow.mainloop()
