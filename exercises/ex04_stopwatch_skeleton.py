# =====================================================
# 연습문제 4 (중급): StopWatch 클래스 + Thread/after 패턴
# -----------------------------------------------------
# 목표: 클래스(상태 관리) + GUI 이벤트 + 주기적 갱신을 결합한다.
#       경과 시간을 0.1초 간격으로 Label 에 표시한다.
#
# 두 가지 방식 모두 가능:
#   (A) threading.Thread + time.sleep   (강의 Code12-12.py 와 같은 형태)
#   (B) window.after(ms, callback)      (tkinter 권장 방식)
#
# 본 문제는 권장되는 (B) after() 방식으로 구현한다.
#
# 주의(오류 가능 지점):
#   * threading 으로 GUI 위젯을 직접 갱신하면 OS 에 따라 충돌/멈춤이 발생할 수 있다.
#     → 가능하면 after() 사용. 꼭 thread 를 써야 한다면 queue.Queue 로 메인 스레드와 통신.
#   * time.sleep() 을 메인 함수에서 호출하면 mainloop 가 멈춰 GUI 가 얼어붙는다.
#   * 시작/정지를 반복해도 누적된 경과시간이 정확히 유지되도록 설계.
# =====================================================

from tkinter import *
import time


## 클래스 선언 부분 ##
class StopWatch:
    def __init__(self):
        self.start_time = None    # 마지막으로 start() 한 시각
        self.elapsed = 0.0        # 누적 경과시간(초)
        self.running = False

    def start(self):
        # TODO: 이미 running 이면 무시
        # TODO: start_time = time.time(), running = True
        pass

    def stop(self):
        # TODO: running 이 False 면 무시
        # TODO: elapsed += time.time() - start_time
        # TODO: running = False
        pass

    def reset(self):
        # TODO: running = False, elapsed = 0.0
        pass

    def current(self):
        """현재까지의 총 경과 시간(초)을 반환"""
        if self.running:
            return self.elapsed + (time.time() - self.start_time)
        else:
            return self.elapsed


## 함수 선언 부분 ##
def update():
    """0.1초마다 자기 자신을 다시 예약해 Label 을 갱신"""
    label.config(text=f"{sw.current():7.2f} 초")
    # TODO: window.after(100, update) 로 자기 자신을 100ms 뒤에 다시 호출
    pass


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

update()           # 주기 갱신 시작
window.mainloop()
