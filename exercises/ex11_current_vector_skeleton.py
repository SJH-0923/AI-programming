# =====================================================
# 연습문제 11 (응용·해양학): 해류 벡터 합성기
# -----------------------------------------------------
# 목표:
#   해류를 동서(u)·남북(v) 성분으로 표현하는 Current 클래스를 만들고,
#   강의 12장의 __add__ 특수 메서드를 오버라이딩해 두 해류를 벡터로 합성한다.
#   합성 결과를 속력·방향으로 환산하고 Canvas 에 화살표로 시각화한다.
#
#   u : 동(+E) 방향 성분 [cm/s]   (서향이면 음수)
#   v : 북(+N) 방향 성분 [cm/s]   (남향이면 음수)
#
#   속력  speed     = sqrt(u² + v²)
#   방향  direction = (degrees(atan2(u, v)) + 360) mod 360
#                     ← 해류가 "흘러가는" 방향, 정북 기준 시계방향
#
# 주의(오류 가능 지점):
#   - 방향 계산에서 atan2(u, v) 순서 주의 (정북 기준이므로 u 가 먼저).
#     일반 수학의 atan2(y, x)=atan2(v, u) 와 다르다!
#   - __add__ 는 반드시 "새 Current 객체" 를 반환해야 한다 (자기 자신을 바꾸지 말 것).
#   - Canvas 의 y 축은 아래로 증가 → 북(+v)을 위로 그리려면 화면 y 는 빼 줘야 한다.
#   - 검증값: u=30,v=40 → speed=50, direction=36.87°
# =====================================================

from tkinter import *
from tkinter import messagebox
import math


## 클래스 선언 부분 ##
class Current:
    def __init__(self, u, v, name=""):
        self.u = u
        self.v = v
        self.name = name

    def speed(self):
        # TODO: sqrt(u² + v²) 반환
        return math.sqrt(self.u**2 + self.v**2)

    def direction(self):
        # TODO: (degrees(atan2(u, v)) + 360) % 360 반환
        return math.degrees(math.atan2(self.u) + 360) % 360 and math.degrees(math.atan2(self.v) + 360) % 360

    def __add__(self, other):
        # TODO: 성분끼리 더한 새 Current 객체 반환 (name 은 "합성")
        return Current(self.u + other.u, self.v + other.v, "합성")

    def __repr__(self):
        return f"Current(u={self.u}, v={self.v}, name={self.name!r})"


## 함수 선언 부분 ##
def on_calc():
    try:
        c1 = Current(float(e_u1.get()), float(e_v1.get()), "해류1")
        c2 = Current(float(e_u2.get()), float(e_v2.get()), "해류2")
    except ValueError:
        messagebox.showerror("입력 오류", "u, v 는 숫자로 입력해 주세요.")
        return

    total = c1 + c2     # __add__ 호출
    result.config(text=(
        f"{c1.name}: {c1.speed():6.2f} cm/s, {c1.direction():6.1f}°\n"
        f"{c2.name}: {c2.speed():6.2f} cm/s, {c2.direction():6.1f}°\n"
        f"합성  : {total.speed():6.2f} cm/s, {total.direction():6.1f}°"
    ))
    draw_vectors(c1, c2, total)


def draw_vectors(c1, c2, total):
    canvas.delete("all")
    W = canvas.winfo_width()
    H = canvas.winfo_height()
    if W < 50 or H < 50:
        return
    ox, oy = W / 2, H / 2          # 원점(화면 중앙)

    # 축
    canvas.create_line(0, oy, W, oy, fill="#dddddd")   # E-W
    canvas.create_line(ox, 0, ox, H, fill="#dddddd")   # N-S
    canvas.create_text(W - 12, oy - 10, text="E", fill="#999999")
    canvas.create_text(ox + 12, 12, text="N", fill="#999999")

    # 스케일: 최대 성분 크기에 맞춰 자동
    mx = max(abs(c1.u), abs(c1.v), abs(c2.u), abs(c2.v),
             abs(total.u), abs(total.v), 1)
    scale = (min(W, H) * 0.4) / mx

    def arrow(cur, color, width=2):
        x2 = ox + cur.u * scale
        y2 = oy - cur.v * scale     # 북(+v)을 위로
        canvas.create_line(ox, oy, x2, y2, fill=color, width=width,
                           arrow=LAST, arrowshape=(12, 14, 5))

    arrow(c1, "blue")
    arrow(c2, "green")
    arrow(total, "red", width=3)


## 메인 코드 부분 ##
window = Tk()
window.title("연습 11 - 해류 벡터 합성기")
window.geometry("460x460")

top = Frame(window); top.pack(pady=8)
Label(top, text="해류1  u:").grid(row=0, column=0, sticky="e")
e_u1 = Entry(top, width=7); e_u1.grid(row=0, column=1); e_u1.insert(0, "30")
Label(top, text="v:").grid(row=0, column=2, sticky="e")
e_v1 = Entry(top, width=7); e_v1.grid(row=0, column=3); e_v1.insert(0, "40")

Label(top, text="해류2  u:").grid(row=1, column=0, sticky="e")
e_u2 = Entry(top, width=7); e_u2.grid(row=1, column=1); e_u2.insert(0, "-20")
Label(top, text="v:").grid(row=1, column=2, sticky="e")
e_v2 = Entry(top, width=7); e_v2.grid(row=1, column=3); e_v2.insert(0, "10")

Button(top, text="합성", width=8, command=on_calc).grid(row=0, column=4, rowspan=2, padx=10)

result = Label(window, text="", font=("Consolas", 11), justify=LEFT)
result.pack()

canvas = Canvas(window, bg="white")
canvas.pack(fill=BOTH, expand=True, padx=10, pady=8)

window.mainloop()
