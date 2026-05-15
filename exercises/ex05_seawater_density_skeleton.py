# =====================================================
# 연습문제 5 (응용/해양학): 해수 밀도 계산기
# -----------------------------------------------------
# 목표: 해양학에서 가장 기본이 되는 해수 밀도 ρ(S, T, 0)
#       (UNESCO 1980 / EOS-80, 압력 = 0 dbar 표면식)을
#       클래스로 캡슐화하고 GUI 에서 사용한다.
#
# 입력:
#   T : 수온 [°C]        (보통 -2 ~ 35)
#   S : 염분 [PSU]       (보통 0 ~ 42)
# 출력:
#   ρ      [kg/m³]
#   σ_t    [kg/m³]  =  ρ - 1000
#
# 공식 (UNESCO 1980, 압력 0):
#   ρ_w(T) = 999.842594 + 6.793952e-2*T - 9.095290e-3*T^2
#            + 1.001685e-4*T^3 - 1.120083e-6*T^4 + 6.536336e-9*T^5
#   A = 8.24493e-1 - 4.0899e-3*T + 7.6438e-5*T^2 - 8.2467e-7*T^3 + 5.3875e-9*T^4
#   B = -5.72466e-3 + 1.0227e-4*T - 1.6546e-6*T^2
#   C = 4.8314e-4
#   ρ(S, T) = ρ_w(T) + A*S + B*S^1.5 + C*S^2
#
# 주의(오류 가능 지점):
#   - 거듭제곱 ** 와 곱셈 * 를 헷갈리지 않도록 주의 (포트란 ** 와 동일)
#   - Entry 에서 받은 문자열은 float() 로 변환 ("23.5" → 23.5). 실패 시 ValueError.
#   - S^1.5 은 S**1.5 이며, S 가 음수면 복소수가 된다.
#     → 유효 범위 (T: -2~40, S: 0~42) 를 클래스에서 검증.
# =====================================================

from tkinter import *
from tkinter import messagebox


## 클래스 선언 부분 ##
class SeaWater:
    """UNESCO 1980 EOS-80 (압력 0 dbar) 기반 해수 밀도 계산기."""

    def __init__(self, T, S):
        # TODO: 유효 범위 검증 (T 는 -2~40, S 는 0~42)
        # 벗어나면 ValueError 발생
        self.T = T
        self.S = S

    def density(self):
        """ρ(S,T,0) [kg/m^3] 반환"""
        T, S = self.T, self.S
        # TODO: 위 공식에 따라 ρ_w, A, B, C 계산
        # TODO: rho = ρ_w + A*S + B*S**1.5 + C*S*S 반환
        pass

    def sigma_t(self):
        """σ_t = ρ - 1000  [kg/m^3]"""
        return self.density() - 1000.0

    def __repr__(self):
        # 강의 12장 __repr__() 와 동일한 패턴
        return f"SeaWater(T={self.T:.2f}°C, S={self.S:.2f}PSU)"


## 함수 선언 부분 ##
def on_calc():
    try:
        T = float(entry_T.get())
        S = float(entry_S.get())
    except ValueError:
        messagebox.showerror("입력 오류", "T와 S는 숫자로 입력해 주세요.")
        return

    try:
        sw = SeaWater(T, S)
    except ValueError as e:
        messagebox.showerror("범위 오류", str(e))
        return

    rho = sw.density()
    sigma = sw.sigma_t()
    result.config(text=f"ρ   = {rho:9.4f} kg/m³\nσ_t = {sigma:9.4f} kg/m³")


## 메인 코드 부분 ##
window = Tk()
window.title("연습 5 - 해수 밀도 계산기 (EOS-80)")
window.geometry("380x230")

Label(window, text="수온 T [°C]:").grid(row=0, column=0, padx=10, pady=8, sticky="e")
entry_T = Entry(window, width=12);  entry_T.grid(row=0, column=1, padx=10, pady=8)
entry_T.insert(0, "15.0")

Label(window, text="염분 S [PSU]:").grid(row=1, column=0, padx=10, pady=8, sticky="e")
entry_S = Entry(window, width=12);  entry_S.grid(row=1, column=1, padx=10, pady=8)
entry_S.insert(0, "34.5")

Button(window, text="계산", width=12, command=on_calc).grid(row=2, column=0, columnspan=2, pady=10)

result = Label(window, text="", font=("Consolas", 12), justify=LEFT)
result.grid(row=3, column=0, columnspan=2)

window.mainloop()
