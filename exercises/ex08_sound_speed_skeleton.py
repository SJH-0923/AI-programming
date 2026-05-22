# =====================================================
# 연습문제 8 (중급·해양학): 해수 중 음속 계산기
# -----------------------------------------------------
# 목표:
#   수온 T, 염분 S, 수심 D 로부터 해수 중 음속 c 를 계산하는
#   Mackenzie(1981) 9항 공식을 클래스로 캡슐화하고 GUI 에서 사용한다.
#   (음향 측심, 소나, 수중 통신의 기본이 되는 값)
#
# 입력:
#   T : 수온 [°C]   (유효 2 ~ 30)
#   S : 염분 [PSU]  (유효 25 ~ 40)
#   D : 수심 [m]    (유효 0 ~ 8000)
#
# Mackenzie(1981) 공식:
#   c = 1448.96 + 4.591*T - 5.304e-2*T^2 + 2.374e-4*T^3
#       + 1.340*(S-35) + 1.630e-2*D + 1.675e-7*D^2
#       - 1.025e-2*T*(S-35) - 7.139e-13*T*D^3
#
# 주의(오류 가능 지점):
#   - T**3, D**3 등 고차항의 부호/지수를 정확히 옮길 것. (검증값으로 확인 가능)
#   - Entry 입력은 문자열 → float 변환 실패 시 ValueError → try/except.
#   - 유효범위를 벗어난 입력은 결과가 비현실적이 되므로 경고를 띄우되 계산은 가능하게 둘지,
#     아예 막을지 정책을 정한다(본 문제는 경고 후 계산).
#   - 검증값: T=25, S=35, D=1000 → c ≈ 1550.744 m/s
# =====================================================

from tkinter import *
from tkinter import messagebox


## 클래스 선언 부분 ##
class SoundSpeed:
    """Mackenzie(1981) 해수 음속 계산기"""

    def __init__(self, T, S, D):
        self.T = T
        self.S = S
        self.D = D

    def in_range(self):
        """유효범위(T 2~30, S 25~40, D 0~8000) 안이면 True"""
        # TODO: 세 조건을 모두 만족하면 True, 아니면 False 반환
        if 2<=self.T and self.T<=30 and 25<=self.S and self.S<=40 and 0<=self.D and self.D<=8000 :
            return True
        else :
            return False

    def speed(self):
        """음속 c [m/s] 반환"""
        T, S, D = self.T, self.S, self.D
        # TODO: 위 Mackenzie 공식 그대로 작성해 c 반환
        c = 1448.96 + 4.591*T - 5.304e-2*T**2 + 2.374e-4*T**3 + 1.340*(S-35) + 1.630e-2*D + 1.675e-7*D**2 - 1.025e-2*T*(S-35) - 7.139e-13*T*D**3
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
