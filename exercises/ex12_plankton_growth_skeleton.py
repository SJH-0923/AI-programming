# =====================================================
# 연습문제 12 (응용·해양학): 플랑크톤 개체군 성장 시뮬레이터
# -----------------------------------------------------
# 목표:
#   로지스틱(logistic) 성장 모형으로 플랑크톤 개체수 N(t) 의 변화를
#   시뮬레이션하는 Population 클래스를 만들고,
#   Scale(슬라이더) 로 성장률 r 을 조절하며 Canvas 에 실시간 곡선을 그린다.
#   (after() 애니메이션 + Scale 위젯 + 클래스의 결합)
#
# 로지스틱 모형:
#   dN/dt = r·N·(1 − N/K)
#   이산화(전진 오일러):  N_{t+1} = N_t + r·N_t·(1 − N_t/K)·Δt
#     r : 내적 성장률,  K : 환경수용력(carrying capacity),  Δt : 시간 간격
#
# 주의(오류 가능 지점):
#   - r·Δt 가 너무 크면 (대략 > 2) 수치해가 진동·발산한다. Δt 를 작게 유지.
#   - Scale 의 값은 get() 으로 읽으며 float 이다. (resolution 설정에 주의)
#   - after() 콜백이 누적 등록되지 않도록 한 곳에서만 재예약할 것
#     (시작 버튼을 여러 번 누르면 콜백이 여러 개 돌 수 있다 → running 플래그로 제어).
#   - Canvas y축은 아래로 증가 → 개체수가 클수록 위로 그리려면 y 를 빼 줄 것.
# =====================================================

from tkinter import *
import math


## 클래스 선언 부분 ##
class Population:
    def __init__(self, N0=5.0, K=1000.0, r=0.5, dt=0.1):
        self.N = N0          # 현재 개체수
        self.K = K           # 환경수용력
        self.r = r           # 성장률
        self.dt = dt
        self.history = [N0]  # 시계열 기록

    def step(self):
        """한 시간 스텝 전진 (로지스틱)"""
        # TODO: dN = r*N*(1 - N/K)*dt 계산 후 self.N 갱신
        # TODO: self.history 에 새 N 추가
        pass

    def reset(self, N0=5.0):
        self.N = N0
        self.history = [N0]


## 함수 선언 부분 ##
running = False
after_id = None


def tick():
    global after_id
    pop.r = scale_r.get()          # 슬라이더에서 성장률 읽기
    pop.step()
    draw()
    if running:
        after_id = window.after(60, tick)


def on_start():
    global running
    if running:
        return                     # 중복 시작 방지
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

    # K 수용력 선
    yK = pad
    canvas.create_line(pad, yK, W - pad, yK, fill="#e0a0a0", dash=(4, 2))
    canvas.create_text(W - pad, yK - 8, anchor="e",
                       text=f"K = {pop.K:.0f}", fill="#c06060", font=("맑은 고딕", 9))

    def to_px(i, N):
        x = pad + (i / max(n - 1, 1)) * (W - 2 * pad)
        y = (H - pad) - (N / pop.K) * (H - 2 * pad)
        return x, y

    # 곡선
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
