# =====================================================
# 연습문제 8 (중급·해양학) - 정답: 해수 중 음속 계산기 (Mackenzie 1981)
# =====================================================
from tkinter import *
from tkinter import messagebox


## 클래스 선언 부분 ##
class SoundSpeed:
    """Mackenzie(1981) 해수 음속 계산기"""

    T_MIN, T_MAX = 2.0, 30.0
    S_MIN, S_MAX = 25.0, 40.0
    D_MIN, D_MAX = 0.0, 8000.0

    def __init__(self, T, S, D):
        self.T = T
        self.S = S
        self.D = D

    def in_range(self):
        return (self.T_MIN <= self.T <= self.T_MAX and
                self.S_MIN <= self.S <= self.S_MAX and
                self.D_MIN <= self.D <= self.D_MAX)

    def speed(self):
        T, S, D = self.T, self.S, self.D
        c = (1448.96
             + 4.591 * T
             - 5.304e-2 * T**2
             + 2.374e-4 * T**3
             + 1.340 * (S - 35)
             + 1.630e-2 * D
             + 1.675e-7 * D**2
             - 1.025e-2 * T * (S - 35)
             - 7.139e-13 * T * D**3)
        return c

    def __repr__(self):
        return f"SoundSpeed(T={self.T}, S={self.S}, D={self.D})"


## 함수 선언 부분 ##
def on_calc():
    try:
        T = float(entry_T.get())
        S = float(entry_S.get())
        D = float(entry_D.get())
    except ValueError:
        messagebox.showerror("입력 오류", "T, S, D 는 숫자로 입력해 주세요.")
        return

    ss = SoundSpeed(T, S, D)
    c = ss.speed()
    result.config(text=f"음속 c = {c:.3f} m/s")

    if not ss.in_range():
        messagebox.showwarning("범위 경고",
            "입력이 Mackenzie 공식 유효범위를 벗어났습니다.\n"
            "(T 2~30 °C, S 25~40 PSU, D 0~8000 m)\n결과는 참고용입니다.")


## 메인 코드 부분 ##
window = Tk()
window.title("연습 8 - 해수 음속 계산기 (Mackenzie 1981)")
window.geometry("400x230")

rows = [("수온 T [°C]:", "25.0"), ("염분 S [PSU]:", "35.0"), ("수심 D [m]:", "1000")]
entries = []
for i, (lab, default) in enumerate(rows):
    Label(window, text=lab).grid(row=i, column=0, padx=10, pady=6, sticky="e")
    e = Entry(window, width=12); e.grid(row=i, column=1, padx=10, pady=6)
    e.insert(0, default)
    entries.append(e)
entry_T, entry_S, entry_D = entries

Button(window, text="계산", width=12, command=on_calc).grid(row=3, column=0, columnspan=2, pady=10)
result = Label(window, text="", font=("Consolas", 13))
result.grid(row=4, column=0, columnspan=2)

window.mainloop()
