# =====================================================
# 연습문제 2 (기초): BankAccount 클래스 + GUI
# -----------------------------------------------------
# 목표: Entry 위젯에서 입력을 받아 클래스 메서드로 처리하고
#       그 결과를 Label 에 표시하는 흐름을 익힌다.
# 요구사항:
#   1) BankAccount 클래스
#        - 클래스 변수 num_accounts (생성된 계좌 총수)
#        - 인스턴스 변수 owner, balance
#        - 메서드 deposit(amount), withdraw(amount), get_balance()
#   2) GUI
#        - Entry 로 금액을 입력
#        - "입금" / "출금" 버튼
#        - 현재 잔액 / 계좌 수를 Label 로 표시
#
# 주의(오류 가능 지점):
#   - Entry.get() 의 반환값은 항상 "문자열" 이다. int(...) 또는 float(...)
#     변환 시 ValueError 가능성 → try/except 또는 .isdigit() 검사 필요.
#   - 음수 입금/출금, 잔액 부족 등의 입력 검증을 클래스 메서드 안에서 처리해
#     예외(ValueError)를 던지면 GUI 쪽이 단순해진다.
#   - messagebox 사용 시 from tkinter import messagebox 가 필요하다.
# =====================================================

from tkinter import *
from tkinter import messagebox


## 클래스 선언 부분 ##
class BankAccount:
    num_accounts = 0   # 정적 변수

    def __init__(self, owner, balance=0):
        # TODO: self.owner, self.balance 초기화
        # TODO: BankAccount.num_accounts 증가
        pass

    def deposit(self, amount):
        # TODO: amount <= 0 이면 ValueError 발생 (메시지: "입금액은 양수여야 합니다")
        # TODO: self.balance 증가
        pass

    def withdraw(self, amount):
        # TODO: amount <= 0 이면 ValueError 발생
        # TODO: 잔액 부족이면 ValueError 발생
        # TODO: self.balance 감소
        pass

    def get_balance(self):
        return self.balance


## 함수 선언 부분 ##
def parse_amount():
    """Entry 에서 정수를 안전하게 꺼낸다. 실패 시 None 반환."""
    text = entry.get().strip()
    # TODO: try/except 로 int 변환, 실패하면 messagebox.showerror 호출 후 None 반환
    pass


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
    # TODO: on_deposit 와 같은 패턴으로 작성
    pass


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
