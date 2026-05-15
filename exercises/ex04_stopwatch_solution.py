# =====================================================
# 연습문제 4 (중급) - 정답: StopWatch 클래스 + after() 패턴
# =====================================================
from tkinter import *
import time


## 클래스 선언 부분 ##
class StopWatch:
    def __init__(self):
        self.start_time = None
        self.elapsed = 0.0
        self.running = False

    def start(self):
        if self.running:
            return
        self.start_time = time.time()
        self.running = True

    def stop(self):
        if not self.running:
            return
        self.elapsed += time.time() - self.start_time
        self.running = False

    def reset(self):
        self.running = False
        self.elapsed = 0.0

    def current(self):
        if self.running:
            return self.elapsed + (time.time() - self.start_time)
        return self.elapsed


## 함수 선언 부분 ##
def update():
    label.config(text=f"{sw.current():7.2f} 초")
    window.after(100, update)   # 100 ms 뒤에 자기 자신을 다시 예약


def on_start():
    sw.start()


def on_stop():
    sw.stop()


def on_reset():
    sw.reset()
    label.config(text=f"{sw.current():7.2f} 초")


## 메인 코드 부분 ##
sw = StopWatch()

window = Tk()
window.title("연습 4 - StopWatch")
window.geometry("320x150")

label = Label(window, text="  0.00 초", font=("Consolas", 28))
label.pack(pady=10)

frm = Frame(window)
frm.pack()
Button(frm, text="시작", width=7, command=on_start).pack(side=LEFT, padx=5)
Button(frm, text="정지", width=7, command=on_stop).pack(side=LEFT, padx=5)
Button(frm, text="리셋", width=7, command=on_reset).pack(side=LEFT, padx=5)

update()
window.mainloop()
