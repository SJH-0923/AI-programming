# =====================================================
# 연습문제 2 (기초) - 정답: BankAccount 클래스 + GUI
# =====================================================
from tkinter import *
from tkinter import messagebox


## 클래스 선언 부분 ##
class BankAccount:
    num_accounts = 0   # 정적 변수

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        BankAccount.num_accounts += 1

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("입금액은 양수여야 합니다.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("출금액은 양수여야 합니다.")
        if amount > self.balance:
            raise ValueError(f"잔액 부족: 현재 {self.balance:,}원")
        self.balance -= amount

    def get_balance(self):
        return self.balance


## 함수 선언 부분 ##
def parse_amount():
    """Entry 에서 정수를 안전하게 꺼낸다."""
    text = entry.get().strip()
    try:
        return int(text)
    except ValueError:
        messagebox.showerror("입력 오류", "금액은 정수로 입력해 주세요.")
        return None


def update_label():
    label.config(
        text=f"소유주: {account.owner}\n잔액: {account.get_balance():,} 원"
              f"\n생성된 계좌 수: {BankAccount.num_accounts}"
    )


def on_deposit():
    amount = parse_amount()
    if amount is None:
        return
    try:
        account.deposit(amount)
    except ValueError as e:
        messagebox.showerror("입금 오류", str(e))
        return
    update_label()


def on_withdraw():
    amount = parse_amount()
    if amount is None:
        return
    try:
        account.withdraw(amount)
    except ValueError as e:
        messagebox.showerror("출금 오류", str(e))
        return
    update_label()


## 메인 코드 부분 ##
account = BankAccount("홍길동", balance=10000)

window = Tk()
window.title("연습 2 - BankAccount + GUI")
window.geometry("360x220")

label = Label(window, text="", font=("맑은 고딕", 12), justify=LEFT)
label.pack(pady=10)

entry = Entry(window, width=15, justify="right")
entry.pack(pady=5)

frm = Frame(window)
frm.pack(pady=5)
Button(frm, text="입금", width=8, command=on_deposit).pack(side=LEFT, padx=5)
Button(frm, text="출금", width=8, command=on_withdraw).pack(side=LEFT, padx=5)

update_label()
window.mainloop()
