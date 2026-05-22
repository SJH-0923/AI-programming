# =====================================================
# 연습문제 9 (중급·해양학): 선형파(미소진폭파) 계산기
# -----------------------------------------------------
# 목표:
#   주기 T 와 수심 h 로부터 선형파 분산관계를 풀어
#   파장 L, 위상속도 c, 군속도 cg 를 구하는 Wave 클래스를 작성.
#   Entry 로 입력받고 Canvas 에 한 파장의 파형(sin)을 그린다.
#
# 분산관계 (g = 9.81):
#   ω = 2π / T
#   ω² = g·k·tanh(k·h)          ← k(파수) 에 대해 비선형 → 반복법으로 해
#   L = 2π / k,   c = L / T,   cg = c/2 · (1 + 2kh / sinh(2kh))
#
# 반복법(뉴턴법) 으로 k 구하기:
#   f(k)  = g·k·tanh(k·h) − ω²
#   f'(k) = g·tanh(k·h) + g·k·h·sech²(k·h)
#   k ← k − f(k)/f'(k)   (수렴할 때까지)
#   초기값: 천해 근사 k0 = ω / sqrt(g·h)
#
# 주의(오류 가능 지점):
#   - math 에는 sech 가 없다. sech(x) = 1/cosh(x) 로 직접 계산.
#   - h 가 매우 크면 tanh(k·h) → 1 (심해), 매우 작으면 천해. 둘 다 잘 동작해야 함.
#   - 0 으로 나누기: T=0 또는 h=0 입력 방지.
#   - 검증값: T=10s, h=1000m(심해) → L≈156.13 m, c≈15.61 m/s
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
        """분산관계를 뉴턴법으로 풀어 파수 k 반환"""
        omega = 2 * math.pi / self.T
        h = self.h
        k = omega / math.sqrt(G * h)    # 천해 초기 추정
        # TODO: 뉴턴 반복으로 k 수렴시키기
        #   f  = G*k*tanh(k*h) - omega**2
        #   df = G*tanh(k*h) + G*k*h*(1/cosh(k*h))**2
        #   k  = k - f/df  (|변화량| < tol 이면 종료)
        
        for _ in range(maxit) :
            tanh = math.tanh(k*h)
            sech2 = (1.0 / math.cosh(k*h))**2
            f = G*k*tanh - omega**2
            df = G*tanh + G*k*h*sech2
            k_new = k - f/df
            if abs(k_new - k) < tol :
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
        # TODO: cg = 0.5*c*(1 + 2*k*h / sinh(2*k*h)) 반환
        cg = 0.5*c*(1 + 2*k*self.h / math.sinh(2*k*self.h))
        return cg

    def regime(self):
        """심해/천해/중간 판정 (h/L 기준)"""
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
    """캔버스에 한 파장(2π) 의 사인파를 그린다."""
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
        phase = 2 * math.pi * px / W      # 화면 폭 = 한 파장
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
