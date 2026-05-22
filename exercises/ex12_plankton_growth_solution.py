# =====================================================
# 연습문제 12 (응용·해양학) - 정답: 플랑크톤 개체군 성장 시뮬레이터
# =====================================================
from tkinter import *


## 클래스 선언 부분 ##
class Population:
    def __init__(self, N0=5.0, K=1000.0, r=0.5, dt=0.1):
        self.N = N0
        self.K = K
        self.r = r
        self.dt = dt
        self.history = [N0]

    def step(self):
        dN = self.r * self.N * (1 - self.N / self.K) * self.dt
        self.N += dN
        self.history.append(self.N)

    def reset(self, N0=5.0):
        self.N = N0
        self.history = [N0]


## 함수 선언 부분 ##
running = False
after_id = None


def tick():
    global after_id
    pop.r = scale_r.get()
    pop.step()
    draw()
    if running:
        after_id = window.after(60, tick)


def on_start():
    global running
    if running:
        return
    running = True
    tick()


def on_pause():
    global running
    running = False


def on_reset():
    global running
    running = False
    pop.reset()
    draw()


def draw():
    canvas.delete("all")
    W = canvas.winfo_width()
    H = canvas.winfo_height()
    if W < 50 or H < 50:
        return
    pad = 40
    hist = pop.history
    n = len(hist)

    yK = pad
    canvas.create_line(pad, yK, W - pad, yK, fill="#e0a0a0", dash=(4, 2))
    canvas.create_text(W - pad, yK - 8, anchor="e",
                       text=f"K = {pop.K:.0f}", fill="#c06060", font=("맑은 고딕", 9))

    def to_px(i, N):
        x = pad + (i / max(n - 1, 1)) * (W - 2 * pad)
        y = (H - pad) - (N / pop.K) * (H - 2 * pad)
        return x, y

    pts = [to_px(i, N) for i, N in enumerate(hist)]
    for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
        canvas.create_line(x1, y1, x2, y2, fill="seagreen", width=2)

    canvas.create_text(pad + 4, pad - 20, anchor="w",
                       text=f"N = {pop.N:8.1f}    r = {pop.r:.2f}    step = {n-1}",
                       font=("Consolas", 10))


## 메인 코드 부분 ##
pop = Population()

window = Tk()
window.title("연습 12 - 플랑크톤 개체군 성장")
window.geometry("560x420")

top = Frame(window); top.pack(fill=X, pady=6)
Button(top, text="시작", width=7, command=on_start).pack(side=LEFT, padx=4)
Button(top, text="정지", width=7, command=on_pause).pack(side=LEFT, padx=4)
Button(top, text="리셋", width=7, command=on_reset).pack(side=LEFT, padx=4)

Label(top, text="성장률 r:").pack(side=LEFT, padx=(20, 2))
scale_r = Scale(top, from_=0.0, to=2.0, resolution=0.05,
                orient=HORIZONTAL, length=180)
scale_r.set(0.5)
scale_r.pack(side=LEFT)

canvas = Canvas(window, bg="white")
canvas.pack(fill=BOTH, expand=True, padx=10, pady=8)

draw()
window.mainloop()
