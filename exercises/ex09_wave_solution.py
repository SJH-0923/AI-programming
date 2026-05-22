# =====================================================
# 연습문제 9 (중급·해양학) - 정답: 선형파(미소진폭파) 계산기
# =====================================================
from tkinter import *
from tkinter import messagebox
import math

G = 9.81


## 클래스 선언 부분 ##
class Wave:
    def __init__(self, period, depth):
        if period <= 0 or depth <= 0:
            raise ValueError("주기 T 와 수심 h 는 0보다 커야 합니다.")
        self.T = period
        self.h = depth

    def wavenumber(self, tol=1e-10, maxit=200):
        omega = 2 * math.pi / self.T
        h = self.h
        k = omega / math.sqrt(G * h)        # 천해 초기 추정
        for _ in range(maxit):
            tanh = math.tanh(k * h)
            sech2 = (1.0 / math.cosh(k * h)) ** 2
            f  = G * k * tanh - omega ** 2
            df = G * tanh + G * k * h * sech2
            k_new = k - f / df
            if abs(k_new - k) < tol:
                k = k_new
                break
            k = k_new
        return k

    def wavelength(self):
        return 2 * math.pi / self.wavenumber()

    def phase_speed(self):
        return self.wavelength() / self.T

    def group_speed(self):
        k = self.wavenumber()
        c = self.phase_speed()
        return 0.5 * c * (1 + 2 * k * self.h / math.sinh(2 * k * self.h))

    def regime(self):
        ratio = self.h / self.wavelength()
        if ratio > 0.5:
            return "심해파 (deep)"
        elif ratio < 0.05:
            return "천해파 (shallow)"
        else:
            return "중간 수심 (intermediate)"


## 함수 선언 부분 ##
def on_calc():
    try:
        T = float(entry_T.get())
        h = float(entry_h.get())
    except ValueError:
        messagebox.showerror("입력 오류", "T 와 h 는 숫자로 입력해 주세요.")
        return
    try:
        w = Wave(T, h)
    except ValueError as e:
        messagebox.showerror("값 오류", str(e))
        return

    L  = w.wavelength()
    c  = w.phase_speed()
    cg = w.group_speed()
    result.config(text=f"L  = {L:8.3f} m\n"
                       f"c  = {c:8.3f} m/s\n"
                       f"cg = {cg:8.3f} m/s\n"
                       f"유형: {w.regime()}")
    draw_wave(L)


def draw_wave(L):
    canvas.delete("all")
    W = canvas.winfo_width()
    H = canvas.winfo_height()
    if W < 50 or H < 50:
        return
    mid = H / 2
    amp = H * 0.3
    canvas.create_line(0, mid, W, mid, fill="#cccccc")
    pts = []
    for px in range(0, W + 1, 2):
        phase = 2 * math.pi * px / W
        y = mid - amp * math.sin(phase)
        pts.append((px, y))
    for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
        canvas.create_line(x1, y1, x2, y2, fill="navy", width=2)
    canvas.create_text(W - 8, 12, anchor="e",
                       text=f"한 파장 L = {L:.1f} m", font=("맑은 고딕", 9))


## 메인 코드 부분 ##
window = Tk()
window.title("연습 9 - 선형파 계산기")
window.geometry("460x360")

top = Frame(window); top.pack(pady=8)
Label(top, text="주기 T [s]:").grid(row=0, column=0, padx=5, pady=4, sticky="e")
entry_T = Entry(top, width=10); entry_T.grid(row=0, column=1, padx=5)
entry_T.insert(0, "10.0")
Label(top, text="수심 h [m]:").grid(row=1, column=0, padx=5, pady=4, sticky="e")
entry_h = Entry(top, width=10); entry_h.grid(row=1, column=1, padx=5)
entry_h.insert(0, "1000")
Button(top, text="계산", width=10, command=on_calc).grid(row=0, column=2, rowspan=2, padx=10)

result = Label(window, text="", font=("Consolas", 11), justify=LEFT)
result.pack()

canvas = Canvas(window, bg="white", height=160)
canvas.pack(fill=BOTH, expand=True, padx=10, pady=8)

window.mainloop()
