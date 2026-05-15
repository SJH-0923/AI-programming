# =====================================================
# 연습문제 7 (응용/해양학): 조석 시뮬레이터
# -----------------------------------------------------
# 목표:
#   1) 조석을 조화분해 한 결과(주요 4개 분조)를 클래스로 모형화
#        Constituent(name, amplitude, period_hr, phase_deg)
#   2) Tide 클래스는 여러 Constituent 를 합쳐 시계열 η(t) 를 만든다.
#   3) Canvas 에 시간에 따른 조위 곡선을 애니메이션으로 그린다.
#        (after() 사용. threading 으로 GUI 갱신은 금지!)
#   4) Checkbutton 으로 각 분조의 켜기/끄기 가능
#
# 주요 분조 표준 주기 (시간):
#   M2  : 12.4206    (반일주 주조석)
#   S2  : 12.0000    (반일주, 태양)
#   K1  : 23.9345    (일주, 달+태양)
#   O1  : 25.8193    (일주, 달)
#
# 식:
#   η(t) = Σ_i  A_i * cos( 2π * t / T_i  -  φ_i )
#   (t: 시간 [hr],  A: 진폭 [m],  T: 주기 [hr],  φ: 위상 [rad])
#
# 주의(오류 가능 지점):
#   * Python math.cos 는 라디안 입력 → 위상을 도(deg) 로 주면 math.radians() 변환 필요.
#   * after(ms, fn) 의 ms 는 정수 (밀리초). 너무 작으면 GUI 가 끊기지 않고 부드럽지만 CPU 사용 증가.
#   * 같은 변수에 새 PhotoImage 등을 매번 할당하면 가비지 컬렉터가 가져가 그림이 안 보일 수 있다.
#     (본 문제에선 직접적이지 않지만 일반 GUI 작성 시 유의)
# =====================================================

from tkinter import *
import math


## 클래스 선언 부분 ##
class Constituent:
    """단일 조화 분조"""
    def __init__(self, name, amplitude, period_hr, phase_deg=0.0):
        self.name = name
        self.A = amplitude
        self.T = period_hr
        self.phi = math.radians(phase_deg)
        self.enabled = True

    def eta(self, t):
        # TODO: A * cos(2π*t/T - φ) 반환 (단, enabled 가 False 면 0)
        pass


class Tide:
    """여러 분조의 합으로 조위를 계산"""

    def __init__(self, constituents):
        self.constituents = constituents

    def eta(self, t):
        # TODO: 각 분조의 eta(t) 를 더해서 총 조위 반환
        pass

    def by_name(self, name):
        for c in self.constituents:
            if c.name == name:
                return c
        return None


## 함수 선언 부분 ##
def toggle(name):
    """체크박스로 분조 on/off"""
    c = tide.by_name(name)
    if c is None:
        return
    c.enabled = bool(check_vars[name].get())


def step():
    """다음 프레임을 그린다 (애니메이션)"""
    global current_t
    current_t += 0.25   # 0.25 시간씩 진행
    draw()
    window.after(50, step)   # 50 ms 마다 갱신


def draw():
    canvas.delete("all")
    W = canvas.winfo_width()
    H = canvas.winfo_height()
    if W < 50 or H < 50:
        return

    # 표시할 시간 창: [current_t - 24h, current_t + 12h]
    t_left  = current_t - 24
    t_right = current_t + 12
    t_span  = t_right - t_left

    pad = 40
    y_mid = H / 2

    # 진폭 자동 결정 (현재 enabled 인 분조의 진폭 합)
    A_total = sum(c.A for c in tide.constituents if c.enabled) + 0.1
    y_scale = (H / 2 - pad) / A_total

    def to_px(t, eta):
        x = pad + (t - t_left) / t_span * (W - 2 * pad)
        y = y_mid - eta * y_scale
        return x, y

    # 가로축 (해수면 0 m 기준선)
    canvas.create_line(pad, y_mid, W - pad, y_mid, fill="#888888", dash=(2, 2))

    # 곡선
    pts = []
    n = 300
    for i in range(n + 1):
        t = t_left + t_span * i / n
        pts.append(to_px(t, tide.eta(t)))
    for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
        canvas.create_line(x1, y1, x2, y2, fill="navy", width=2)

    # 현재 시각 (수직선)
    x_now, _ = to_px(current_t, 0)
    canvas.create_line(x_now, pad, x_now, H - pad, fill="red", width=1, dash=(4, 2))
    eta_now = tide.eta(current_t)
    canvas.create_text(x_now + 10, pad + 10,
                       text=f"t = {current_t:6.2f} h\nη = {eta_now:+.3f} m",
                       anchor="w", font=("Consolas", 10))


## 메인 코드 부분 ##
tide = Tide([
    Constituent("M2", 0.80, 12.4206, 0),
    Constituent("S2", 0.30, 12.0000, 30),
    Constituent("K1", 0.25, 23.9345, 60),
    Constituent("O1", 0.18, 25.8193, 90),
])

current_t = 0.0

window = Tk()
window.title("연습 7 - 조석 시뮬레이터")
window.geometry("640x460")

# 분조 on/off 체크박스
top = Frame(window)
top.pack(fill=X)
check_vars = {}
for c in tide.constituents:
    v = IntVar(value=1)
    check_vars[c.name] = v
    Checkbutton(top, text=f"{c.name}  A={c.A:.2f}m T={c.T:.2f}h",
                variable=v, command=lambda n=c.name: toggle(n)).pack(side=LEFT, padx=5)

# 그래프
canvas = Canvas(window, bg="white")
canvas.pack(fill=BOTH, expand=True, padx=10, pady=10)

step()        # 애니메이션 시작
window.mainloop()
