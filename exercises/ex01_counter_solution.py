# =====================================================
# 연습문제 1 (기초) - 정답: Counter 클래스 + GUI
# =====================================================
from tkinter import *


## 클래스 선언 부분 ##
class Counter:
    total_clicks = 0   # 클래스(정적) 변수

    def __init__(self, start=0):
        self.value = start

    def increment(self):
        self.value += 1
        Counter.total_clicks += 1     # 클래스 변수는 ClassName.변수 로 접근

    def decrement(self):
        self.value -= 1
        Counter.total_clicks += 1

    def reset(self):
        self.value = 0
        # total_clicks 는 의도적으로 유지


## 함수 선언 부분 ##
def update_label():
    label.config(
        text=f"현재 값: {counter.value}   /   총 클릭수: {Counter.total_clicks}"
    )


def on_plus():
    counter.increment()
    update_label()


def on_minus():
    counter.decrement()
    update_label()


def on_reset():
    counter.reset()
    update_label()


## 메인 코드 부분 ##
counter = Counter(start=0)

window = Tk()
window.title("연습 1 - Counter 클래스 + GUI")
window.geometry("360x150")

label = Label(window, text="", font=("맑은 고딕", 14))
label.pack(pady=10)

btn_plus  = Button(window, text="+",   width=6, command=on_plus)
btn_minus = Button(window, text="-",   width=6, command=on_minus)
btn_reset = Button(window, text="Reset", width=8, command=on_reset)

btn_plus.pack(side=LEFT,  padx=10, pady=10)
btn_minus.pack(side=LEFT, padx=10, pady=10)
btn_reset.pack(side=LEFT, padx=10, pady=10)

update_label()
window.mainloop()
