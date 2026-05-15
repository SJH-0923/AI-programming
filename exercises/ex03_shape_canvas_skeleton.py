# =====================================================
# 연습문제 3 (중급): Shape 상속 + Canvas + Radiobutton
# -----------------------------------------------------
# 목표: Shape 슈퍼클래스를 두고 Circle / Rectangle / Triangle 가 상속받아
#       draw() 를 오버라이딩 하도록 만든다.
#       Radiobutton 으로 도형을 선택하고, Canvas 를 클릭하면 그 위치에 그린다.
#
# 주의(오류 가능 지점):
#   - super().__init__() 호출을 빠뜨리면 부모 클래스의 인스턴스 변수가 만들어지지 않는다.
#   - tkinter Canvas 좌표계는 좌상단이 (0,0) 이고 y는 아래로 증가한다.
#     수학 좌표와 부호가 반대임을 유의.
#   - Radiobutton 그룹은 같은 IntVar / StringVar 를 공유해야만 묶인다.
# =====================================================

from tkinter import *
import random


## 클래스 선언 부분 ##
class Shape:
    """슈퍼 클래스: 추상 메서드 draw() 만 정의"""
    def __init__(self, canvas, x, y, color=None):
        # TODO: 인자 저장 (self.canvas, self.x, self.y)
        # TODO: color 가 None 이면 무작위 색 (예: random_color()) 사용
        pass

    def draw(self):
        # 자식 클래스가 반드시 override 해야 한다
        raise NotImplementedError("Shape.draw() 를 override 하세요.")


def random_color():
    return "#%02x%02x%02x" % (random.randint(0, 255),
                              random.randint(0, 255),
                              random.randint(0, 255))


class Circle(Shape):
    def __init__(self, canvas, x, y, r=30, color=None):
        super().__init__(canvas, x, y, color)
        self.r = r

    def draw(self):
        # TODO: canvas.create_oval(x-r, y-r, x+r, y+r, fill=self.color) 호출
        pass


class Rectangle(Shape):
    def __init__(self, canvas, x, y, w=60, h=40, color=None):
        super().__init__(canvas, x, y, color)
        self.w = w
        self.h = h

    def draw(self):
        # TODO: canvas.create_rectangle(...) 호출
        pass


class Triangle(Shape):
    def __init__(self, canvas, x, y, size=40, color=None):
        super().__init__(canvas, x, y, color)
        self.size = size

    def draw(self):
        # TODO: 세 꼭짓점 좌표를 만들어 canvas.create_polygon(...) 호출
        # 예: 정삼각형이 (x,y) 를 중심으로 그려지도록
        pass


## 함수 선언 부분 ##
def on_canvas_click(event):
    """캔버스를 클릭하면 현재 선택된 도형을 그 위치에 그린다."""
    kind = shape_var.get()
    if kind == 1:
        shape = Circle(canvas, event.x, event.y)
    elif kind == 2:
        shape = Rectangle(canvas, event.x, event.y)
    else:
        shape = Triangle(canvas, event.x, event.y)
    shape.draw()


def on_clear():
    canvas.delete("all")


## 메인 코드 부분 ##
window = Tk()
window.title("연습 3 - Shape 상속 + Canvas")
window.geometry("520x460")

shape_var = IntVar(value=1)   # 라디오 그룹 공유 변수

frm_top = Frame(window)
frm_top.pack(side=TOP, fill=X)

Radiobutton(frm_top, text="원",       variable=shape_var, value=1).pack(side=LEFT, padx=5, pady=5)
Radiobutton(frm_top, text="사각형",   variable=shape_var, value=2).pack(side=LEFT, padx=5, pady=5)
Radiobutton(frm_top, text="삼각형",   variable=shape_var, value=3).pack(side=LEFT, padx=5, pady=5)
Button(frm_top, text="지우기", command=on_clear).pack(side=RIGHT, padx=5, pady=5)

canvas = Canvas(window, bg="white")
canvas.pack(fill=BOTH, expand=True)
canvas.bind("<Button-1>", on_canvas_click)

window.mainloop()
