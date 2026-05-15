# =====================================================
# 연습문제 6 (응용/해양학): CTD 데이터 뷰어
# -----------------------------------------------------
# 목표:
#   1) CSV 파일에서 (수심, 수온, 염분) 데이터를 읽어 CTD 클래스 객체로 보관
#   2) tkinter Menu "파일 > 열기 / 종료" 로 데이터 파일을 선택
#   3) Canvas 에 수온/염분의 수직 프로파일을 두 색으로 그린다
#   4) Radiobutton 으로 어떤 변수를 그릴지 전환
#
# 입력 CSV 형식 (header 1줄, 단위 포함):
#   depth_m,temperature_C,salinity_PSU
#   0,22.50,33.80
#   ...
#
# 주의(오류 가능 지점):
#   * Canvas 좌표는 y 가 아래로 증가 → 수심도 아래로 증가하므로 그대로 그려도 자연스럽다.
#     단, 수온/염분 축은 좌표 변환을 잘 해 주어야 한다.
#   * Entry 가 아니라 파일에서 읽을 때도 변환 실패(ValueError)는 항상 가능 → try/except.
#   * 윈도 크기가 바뀌어도 다시 그릴 수 있도록 draw_profile() 을 함수로 분리.
#   * 사용 예: 이 파일과 같은 폴더의 sample_ctd.csv 를 열어 보세요.
# =====================================================

from tkinter import *
from tkinter import filedialog, messagebox
import csv


## 클래스 선언 부분 ##
class CTD:
    """CTD 캐스트 한 회 분 데이터 (수심, 수온, 염분)"""

    def __init__(self, depth=None, temperature=None, salinity=None, name=""):
        self.depth = depth or []        # m
        self.temperature = temperature or []   # °C
        self.salinity = salinity or []  # PSU
        self.name = name

    @classmethod
    def from_csv(cls, path):
        """CSV 파일에서 CTD 객체 생성 (분류 메서드 = classmethod 사용 예)"""
        depth, temp, sal = [], [], []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)   # header 행 건너뛰기
            for row in reader:
                if not row:
                    continue
                # TODO: row[0]→depth, row[1]→temperature, row[2]→salinity
                # TODO: float 로 변환해서 리스트에 append
                pass
        return cls(depth, temp, sal, name=path.split("/")[-1])

    def avg_T(self):
        # TODO: 수온 평균. 데이터가 없으면 0 반환
        pass

    def avg_S(self):
        # TODO: 염분 평균
        pass

    def max_depth(self):
        return max(self.depth) if self.depth else 0.0


## 함수 선언 부분 ##
ctd = None     # 현재 표시 중인 CTD 객체


def open_file():
    global ctd
    path = filedialog.askopenfilename(
        parent=window,
        title="CTD CSV 파일 열기",
        filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*"))
    )
    if not path:
        return
    try:
        ctd = CTD.from_csv(path)
    except Exception as e:
        messagebox.showerror("파일 오류", f"파일을 읽지 못했습니다.\n{e}")
        return

    info.config(
        text=f"파일: {ctd.name}\n"
             f"포인트 수: {len(ctd.depth)}    최대 수심: {ctd.max_depth():.1f} m\n"
             f"평균 수온: {ctd.avg_T():.2f} °C    평균 염분: {ctd.avg_S():.2f} PSU"
    )
    draw_profile()


def exit_app():
    window.quit()
    window.destroy()


def draw_profile(*_):
    canvas.delete("all")
    if ctd is None or not ctd.depth:
        return

    var = var_choice.get()    # 1: 수온, 2: 염분
    values = ctd.temperature if var == 1 else ctd.salinity
    color  = "red" if var == 1 else "blue"
    label_text = "수온 [°C]" if var == 1 else "염분 [PSU]"

    W = canvas.winfo_width()
    H = canvas.winfo_height()
    if W < 50 or H < 50:
        return

    pad = 50
    x_min, x_max = min(values) - 0.5, max(values) + 0.5
    d_min, d_max = 0, ctd.max_depth()

    def to_px(v, d):
        x = pad + (v - x_min) / (x_max - x_min) * (W - 2 * pad)
        y = pad + (d - d_min) / (d_max - d_min) * (H - 2 * pad)
        return x, y

    # 축
    canvas.create_rectangle(pad, pad, W - pad, H - pad, outline="black")
    canvas.create_text(W / 2, 20, text=label_text, font=("맑은 고딕", 11, "bold"))
    canvas.create_text(20, H / 2, text="수심 [m]", angle=90, font=("맑은 고딕", 11, "bold"))

    # 데이터 라인
    pts = []
    for v, d in zip(values, ctd.depth):
        pts.append(to_px(v, d))
    for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
        canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
    for x, y in pts:
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outline="")


## 메인 코드 부분 ##
window = Tk()
window.title("연습 6 - CTD Profile Viewer")
window.geometry("600x520")

# 메뉴
menubar = Menu(window)
window.config(menu=menubar)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="파일", menu=filemenu)
filemenu.add_command(label="열기 ...", command=open_file)
filemenu.add_separator()
filemenu.add_command(label="종료", command=exit_app)

# 정보 영역
info = Label(window, text="파일을 열어 주세요.", justify=LEFT, anchor="w",
             font=("맑은 고딕", 10))
info.pack(fill=X, padx=10, pady=5)

# 변수 선택
var_choice = IntVar(value=1)
frm = Frame(window)
frm.pack(anchor="w", padx=10)
Radiobutton(frm, text="수온",  variable=var_choice, value=1, command=draw_profile).pack(side=LEFT)
Radiobutton(frm, text="염분",  variable=var_choice, value=2, command=draw_profile).pack(side=LEFT)

# 그래프 영역
canvas = Canvas(window, bg="white")
canvas.pack(fill=BOTH, expand=True, padx=10, pady=10)
canvas.bind("<Configure>", draw_profile)   # 창 크기가 바뀌면 다시 그림

window.mainloop()
