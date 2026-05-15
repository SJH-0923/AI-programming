# =====================================================
# 연습문제 1 (기초): Counter 클래스 + GUI
# -----------------------------------------------------
# 목표: 클래스 인스턴스를 GUI 버튼과 연결하는 기본 패턴을 익힌다.
# 요구사항:
#   1) Counter 클래스에 인스턴스 변수 value(현재 값)와
#      클래스(정적) 변수 total_clicks(모든 객체가 공유하는 총 클릭수)를 둔다.
#   2) increment(), decrement(), reset() 메서드를 작성한다.
#   3) tkinter GUI로 "+", "-", "Reset" 버튼을 만들고
#      Label에 현재 값과 총 클릭수를 표시한다.
#
# 주의(오류 가능 지점):
#   - 클래스 변수를 self.total_clicks 로만 다루면 인스턴스 변수가 생성되어
#     "공유" 효과가 깨진다. 반드시 Counter.total_clicks 로 갱신할 것.
#   - Label 텍스트는 label.config(text=...) 또는 StringVar 로 갱신한다.
# =====================================================

from tkinter import *


## 클래스 선언 부분 ##
class Counter:
    total_clicks = 0   # 클래스(정적) 변수: 모든 객체가 공유

    def __init__(self, start=0):
        self.value = start   # 인스턴스 변수

    def increment(self):
        # TODO: self.value 를 1 증가시키고
        self.value += 1
        #       Counter.total_clicks 도 1 증가시켜라
        pass

    def decrement(self):
        # TODO: self.value 를 1 감소시키고
        self.value -= 1
        #       Counter.total_clicks 도 1 증가시켜라
        if self.value < 0 :
            self.value = 0
        pass

    def reset(self):
        # TODO: self.value 를 0 으로 만들어라
        self.value = 0
        #       (total_clicks 는 유지)
        pass


## 함수 선언 부분 ##
def update_label():
    """Label 위젯의 텍스트를 현재 카운터 상태로 갱신"""
    # TODO: label.config(text=...) 를 사용해 다음 형식으로 표시
    label.config(text = f"현재 값 : {counter.value} / 총 클릭 수 : {counter.total_clicks}")
    #       "현재 값: {value}   /   총 클릭수: {total_clicks}"
    pass


def on_plus():
    counter.increment()
    update_label()


def on_minus():
    # TODO: 빈칸 채우기
    counter.decrement()
    update_label()
    pass


def on_reset():
    # TODO: 빈칸 채우기
    counter.reset()
    update_label()
    pass


## 메인 코드 부분 ##
counter = Counter(start=0)

window = Tk()
window.title("연습 1 - Counter 클래스 + GUI")
window.geometry("360x150")

label = Label(window, text="", font=("맑은 고딕", 14))
label.pack(pady=10)

btn_plus  = Button(window, text="+", width=6, command=on_plus)
btn_minus = Button(window, text="-", width=6, command=on_minus)
btn_reset = Button(window, text="Reset", width=8, command=on_reset)

btn_plus.pack(side=LEFT,  padx=10, pady=10)
btn_minus.pack(side=LEFT, padx=10, pady=10)
btn_reset.pack(side=LEFT, padx=10, pady=10)

update_label()
window.mainloop()
