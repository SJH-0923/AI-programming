# =====================================================
# 연습문제 5 (응용/해양학) - 정답: 해수 밀도 계산기 (EOS-80, P=0)
# =====================================================
from tkinter import *
from tkinter import messagebox


## 클래스 선언 부분 ##
class SeaWater:
    """UNESCO 1980 EOS-80 (압력 0 dbar) 해수 밀도 계산기"""

    T_MIN, T_MAX = -2.0, 40.0
    S_MIN, S_MAX =  0.0, 42.0

    def __init__(self, T, S):
        if not (self.T_MIN <= T <= self.T_MAX):
            raise ValueError(f"T 는 {self.T_MIN}~{self.T_MAX} °C 범위여야 합니다.")
        if not (self.S_MIN <= S <= self.S_MAX):
            raise ValueError(f"S 는 {self.S_MIN}~{self.S_MAX} PSU 범위여야 합니다.")
        self.T = T
        self.S = S

    def density(self):
        T, S = self.T, self.S

        # 순수 물 밀도 (S = 0)
        rho_w = (999.842594
                 + 6.793952e-2 * T
                 - 9.095290e-3 * T**2
                 + 1.001685e-4 * T**3
                 - 1.120083e-6 * T**4
                 + 6.536336e-9 * T**5)

        A = (8.24493e-1
             - 4.0899e-3 * T
             + 7.6438e-5 * T**2
             - 8.2467e-7 * T**3
             + 5.3875e-9 * T**4)

        B = (-5.72466e-3
             + 1.0227e-4 * T
             - 1.6546e-6 * T**2)

        C = 4.8314e-4

        rho = rho_w + A * S + B * S**1.5 + C * S * S
        return rho

    def sigma_t(self):
        return self.density() - 1000.0

    def __repr__(self):
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

    rho   = sw.density()
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
