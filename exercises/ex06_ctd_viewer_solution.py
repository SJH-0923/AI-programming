# =====================================================
# 연습문제 6 (응용/해양학) - 정답: CTD 데이터 뷰어
# =====================================================
from tkinter import *
from tkinter import filedialog, messagebox
import csv


## 클래스 선언 부분 ##
class CTD:
    """CTD 캐스트 한 회 분 데이터 (수심, 수온, 염분)"""

    def __init__(self, depth=None, temperature=None, salinity=None, name=""):
        self.depth       = depth       if depth       is not None else []
        self.temperature = temperature if temperature is not None else []
        self.salinity    = salinity    if salinity    is not None else []
        self.name = name

    @classmethod
    def from_csv(cls, path):
        depth, temp, sal = [], [], []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)  # 헤더 행
            for row in reader:
                if not row:
                    continue
                depth.append(float(row[0]))
                temp.append(float(row[1]))
                sal.append(float(row[2]))
        return cls(depth, temp, sal, name=path.split("/")[-1])

    def avg_T(self):
        return sum(self.temperature) / len(self.temperature) if self.temperature else 0.0

    def avg_S(self):
        return sum(self.salinity) / len(self.salinity) if self.salinity else 0.0

    def max_depth(self):
        return max(self.depth) if self.depth else 0.0

    def __repr__(self):
        return f"CTD(n={len(self.depth)}, name={self.name!r})"


## 함수 선언 부분 ##
ctd = None


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

    var = var_choice.get()
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

    # 외곽 박스 + 축 라벨
    canvas.create_rectangle(pad, pad, W - pad, H - pad, outline="black")
    canvas.create_text(W / 2, 20, text=label_text, font=("맑은 고딕", 11, "bold"))
    canvas.create_text(20, H / 2, text="수심 [m]", angle=90, font=("맑은 고딕", 11, "bold"))

    # X축 눈금
    for k in range(5):
        v = x_min + (x_max - x_min) * k / 4
        x, _ = to_px(v, d_min)
        canvas.create_line(x, pad, x, H - pad, fill="#dddddd")
        canvas.create_text(x, H - pad + 12, text=f"{v:.1f}", font=("Consolas", 8))

    # Y축 눈금
    for k in range(5):
        d = d_min + (d_max - d_min) * k / 4
        _, y = to_px(x_min, d)
        canvas.create_line(pad, y, W - pad, y, fill="#dddddd")
        canvas.create_text(pad - 8, y, text=f"{d:.0f}", font=("Consolas", 8), anchor="e")

    # 데이터 라인 + 점
    pts = [to_px(v, d) for v, d in zip(values, ctd.depth)]
    for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
        canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
    for x, y in pts:
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outline="")


## 메인 코드 부분 ##
window = Tk()
window.title("연습 6 - CTD Profile Viewer")
window.geometry("600x520")

menubar = Menu(window)
window.config(menu=menubar)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="파일", menu=filemenu)
filemenu.add_command(label="열기 ...", command=open_file)
filemenu.add_separator()
filemenu.add_command(label="종료", command=exit_app)

info = Label(window, text="파일을 열어 주세요. (예: sample_ctd.csv)",
             justify=LEFT, anchor="w", font=("맑은 고딕", 10))
info.pack(fill=X, padx=10, pady=5)

var_choice = IntVar(value=1)
frm = Frame(window)
frm.pack(anchor="w", padx=10)
Radiobutton(frm, text="수온", variable=var_choice, value=1, command=draw_profile).pack(side=LEFT)
Radiobutton(frm, text="염분", variable=var_choice, value=2, command=draw_profile).pack(side=LEFT)

canvas = Canvas(window, bg="white")
canvas.pack(fill=BOTH, expand=True, padx=10, pady=10)
canvas.bind("<Configure>", draw_profile)

window.mainloop()
