from tkinter import *
from tkinter import messagebox
import random as rd



#클래스 생성
class WeaponEnhancer :
    def __init__(self) :
        self.level = 0
        self.grade = ["0강", "1강", "2강", "3강", "4강", "5강", "6강", "7강", "8강", "9강", "10강"]
        self.prob = [1.0, 0.9, 0.8, 0.7, 0.5, 0.4, 0.3, 0.15, 0.05, 0.01]

    #강화 함수
    def enhance(self) :
        if self.level == 10 :
            messagebox.showinfo("", "!강화 최대치입니다!") 
            return

        dice = rd.random()      #random을 사용해서 0에서 1 사이 숫자 뽑음

        if dice < self.prob[self.level] :
            self.level += 1     #레벨 하나 올림
            messagebox.showinfo("", f"강화 성공! +1강 (현재 {self.grade[self.level]})")

            weapon_image = PhotoImage(file=f"sword_pic/{self.level}.png")
            self.photo_label.config(image = weapon_image)
            self.photo_label.image = weapon_image

            return

        else :
            self.level = 0      #레벨 초기화
            messagebox.showinfo("", "강화 실패! 무기가 파괴되었습니다...")

            weapon_image = PhotoImage(file=f"sword_pic/{self.level}.png")
            self.photo_label.config(image = weapon_image)
            self.photo_label.image = weapon_image

            return

weapon = WeaponEnhancer()



window = Tk()
window.title("검 키우기 게임")
window.geometry("500x700")

title = Label(window, text = "⚔️ 검 키우기 ⚔️", font = ("맑은 고딕", 20, "bold"))
title.pack(pady = 10)

initial_image = PhotoImage(file=f"sword_pic/{weapon.level}.png")
photo = Label(window, image = initial_image)
photo.pack(pady = 10)
weapon.photo_label = photo

label = Label(window, text = "")
label.pack(pady = 20)

button_enhance = Button(window, text = "🔥 강화 🔥", font = ("맑은 고딕", 13, "bold"), fg = "red", command = weapon.enhance)
button_quit = Button(window, text = "게임종료", font = ("맑은 고딕", 13, "bold"), command = quit)
button_enhance.pack(pady = 20)
button_quit.pack(pady = 20)

window.mainloop()
