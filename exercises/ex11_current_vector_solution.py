# =====================================================
# 연습문제 11 (응용·해양학) - 정답: 해류 벡터 합성기
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
        return math.sqrt(self.u ** 2 + self.v ** 2)

    def direction(self):
        return (math.degrees(math.atan2(self.u, self.v)) + 360) % 360

    def __add__(self, other):
        return Current(self.u + other.u, self.v + other.v, name="합성")

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

    total = c1 + c2
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
    ox, oy = W / 2, H / 2

    canvas.create_line(0, oy, W, oy, fill="#dddddd")
    canvas.create_line(ox, 0, ox, H, fill="#dddddd")
    canvas.create_text(W - 12, oy - 10, text="E", fill="#999999")
    canvas.create_text(ox + 12, 12, text="N", fill="#999999")

    mx = max(abs(c1.u), abs(c1.v), abs(c2.u), abs(c2.v),
             abs(total.u), abs(total.v), 1)
    scale = (min(W, H) * 0.4) / mx

    def arrow(cur, color, width=2):
        x2 = ox + cur.u * scale
        y2 = oy - cur.v * scale
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
