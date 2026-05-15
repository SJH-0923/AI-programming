# =====================================================
# 연습문제 3 (중급) - 정답: Shape 상속 + Canvas + Radiobutton
# =====================================================
from tkinter import *
import random


def random_color():
    return "#%02x%02x%02x" % (random.randint(0, 255),
                              random.randint(0, 255),
                              random.randint(0, 255))


## 클래스 선언 부분 ##
class Shape:
    def __init__(self, canvas, x, y, color=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color if color is not None else random_color()

    def draw(self):
        raise NotImplementedError("Shape.draw() 를 override 하세요.")


class Circle(Shape):
    def __init__(self, canvas, x, y, r=30, color=None):
        super().__init__(canvas, x, y, color)
        self.r = r

    def draw(self):
        x, y, r = self.x, self.y, self.r
        self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                fill=self.color, outline="")


class Rectangle(Shape):
    def __init__(self, canvas, x, y, w=60, h=40, color=None):
        super().__init__(canvas, x, y, color)
        self.w = w
        self.h = h

    def draw(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        self.canvas.create_rectangle(x - w / 2, y - h / 2,
                                     x + w / 2, y + h / 2,
                                     fill=self.color, outline="")


class Triangle(Shape):
    def __init__(self, canvas, x, y, size=40, color=None):
        super().__init__(canvas, x, y, color)
        self.size = size

    def draw(self):
        x, y, s = self.x, self.y, self.size
        # 정삼각형 (위쪽 꼭짓점이 위로 향함)
        p1 = (x,         y - s)
        p2 = (x - s,     y + s * 0.7)
        p3 = (x + s,     y + s * 0.7)
        self.canvas.create_polygon(p1, p2, p3,
                                   fill=self.color, outline="")


## 함수 선언 부분 ##
def on_canvas_click(event):
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

shape_var = IntVar(value=1)

frm_top = Frame(window)
frm_top.pack(side=TOP, fill=X)

Radiobutton(frm_top, text="원",     variable=shape_var, value=1).pack(side=LEFT, padx=5, pady=5)
Radiobutton(frm_top, text="사각형", variable=shape_var, value=2).pack(side=LEFT, padx=5, pady=5)
Radiobutton(frm_top, text="삼각형", variable=shape_var, value=3).pack(side=LEFT, padx=5, pady=5)
Button(frm_top, text="지우기", command=on_clear).pack(side=RIGHT, padx=5, pady=5)

canvas = Canvas(window, bg="white")
canvas.pack(fill=BOTH, expand=True)
canvas.bind("<Button-1>", on_canvas_click)

window.mainloop()
