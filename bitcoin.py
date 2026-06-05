#턴 넘기기
#기본 자산 : 1,000,000원 / 보유 코인 0
#승리 조건 : 20턴 내에 자산 10,000,000원 달성 or 파산 안 하기
#패배 조건 : 20턴 지났는데 10,000,000 달성 실패 or 파산
#호재 (Bull) / 신제품 대박 or 일론 머스크 트윗 / 폭등 (+30%)
#평온 (Normal) / 횡보 중 or 평이한 실적 발표 / 상승 (+10%)
#악재 (Bear) / 서버 마비 or 대표이사 횡령 / 하락 (-15%)
#대공황 (Panic)	/ 거래소 해킹 or 상장 폐지 위기 / 폭락 (-50%)
#random.choice()로 시장의 상태를 결정
#처음 시작>매도or 매수 결정>턴 넘기기>뉴스가 뜸 : 반복 실행


from tkinter import *
from tkinter import messagebox
import random as rd


global_coin = None
global_day = None
global_trend = "Normal"
price_history = [100000]



def refresh_ui():
    coin_chart.config(text=f"📊 현재 코인 시세: {global_coin.price:,}원")

    try:
        asset_label.config(text=f"📅 {global_day.day}일차 | 💵 잔고: {my_asset.money:,}원 | 🪙 보유 코인: {my_asset.coin_count}개")
    except:
        pass
    
    draw_chart()



def draw_chart() :
    chart_canvas.delete("all")
    W = chart_canvas.winfo_width()
    H = chart_canvas.winfo_height()

    if W < 50 :
        w = 450
    if H < 50 :
        H = 150
        
    mid = H / 2
    
    chart_canvas.create_line(0, mid, W, mid, fill="#cccccc", dash=(4, 2))
    
    
    pts = []


    x_interval = W / 20 
    
    for day_idx, price in enumerate(price_history):
        
        px = day_idx * x_interval
        
        y = mid - (price - 100000) / 50000 * (H * 0.4)
        
        if y < 10: y = 10
        if y > H - 10: y = H - 10
        
        pts.append((px, y))

    if len(pts) >= 2 :
        for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
            chart_canvas.create_line(x1, y1, x2, y2, fill="red", width=3)

    chart_canvas.create_text(W - 8, 15, anchor="e", text=f"현재가: {global_coin.price:,} 원", font=("맑은 고딕", 10, "bold"), fill="#333333")




class Coin :
    def __init__(self) :
        self.price = 100000
    
    def update_status(self) :
        if self.price < 500:
            self.price = 500
    
        if self.price >= 10000000 :
            messagebox.showinfo("", "🚀 You Are Rich ! 🚀")


class Asset :
    def __init__(self) :
        self.money = 1000000
        self.coin_count = 0

    def buy(self):
        if self.money >= global_coin.price :
            self.money -= global_coin.price
            self.coin_count += 1
            messagebox.showinfo("", f"매수 완료! 남은 현금: {self.money}원 / 보유 코인: {self.coin_count}개")
        else :
            print("", "❌ 잔액이 부족합니다! ❌")
        
        refresh_ui()

    def sell(self):
        if self.coin_count > 0:
            self.money += global_coin.price
            self.coin_count -= 1
            messagebox.showinfo("", f"매도 완료! 남은 현금: {self.money}원 / 보유 코인: {self.coin_count}개")
        else:
            messagebox.showinfo("", "❌ 매도할 코인이 없습니다!")
        
        refresh_ui()

class Day :
    def __init__(self) :
        self.day = 1

    def next_day(self) :
        self.day += 1
        print(f"{self.day}일차")

        if self.day > 20 :
            messagebox.showinfo("", "💀 Game Over 💀")
            window.quit()

class News :
    def __init__(self) :
        self.news_pool = {"Greedy": [], "Good": [], "So-So": [], "Bad": [], "Panic": []}

        try :
            with open("news_data.txt", "r", encoding="utf-8") as file :
                for line in file :
                    line = line.strip()
                    if not line or "|" not in line :
                        continue

                    grade, content, change_rate = line.split("|")
                    self.news_pool[grade].append([content, float(change_rate)])

        except FileNotFoundError :
            print("news_data.txt 파일을 찾을 수 없습니다.")

    def next_day_news(self) :
        global global_trend
        
        grades = ["Greedy", "Good", "So-So", "Bad", "Panic"]

        '''
        grades = ["Greedy", "Good", "So-So", "Bad", "Panic"]
        probabilities = [0.05, 0.25, 0.40, 0.25, 0.05]
        
        selected_grade = rd.choices(grades, weights = probabilities, k=1)[0]
        '''
        
        if global_trend == "Bull":
            # 불장일 때는 호재(Greedy, Good) 확률 대폭 상승 (도합 60%)
            probabilities = [0.15, 0.45, 0.25, 0.12, 0.03]
        elif global_trend == "Bear":
            # 폭락장일 때는 악재(Bad, Panic) 확률 대폭 상승 (도합 60%)
            probabilities = [0.03, 0.12, 0.25, 0.45, 0.15]
        else:
            # 일반(Normal) 상태일 때는 원래 설계했던 평범한 확률
            probabilities = [0.05, 0.25, 0.40, 0.25, 0.05]

        # 확률 가중치를 반영해서 오늘 뜰 뉴스 등급 추첨
        selected_grade = rd.choices(grades, weights=probabilities, k=1)[0]

        # [Step 2] 오늘 뽑힌 등급을 보고 '다음 날 시장 분위기'를 미리 세팅! (연계성 핵심)
        if selected_grade in ["Greedy", "Good"]:
            global_trend = "Bull"    # 좋은 뉴스 뜨면 다음 날부터 불장 시작
        elif selected_grade in ["Panic", "Bad"]:
            global_trend = "Bear"    # 나쁜 뉴스 뜨면 다음 날부터 하락장 시작
        else:
            global_trend = "Normal"  # 평범한 뉴스면 일반 상태로 복귀




        chosen_news = rd.choice(self.news_pool[selected_grade])
        content, change_rate = chosen_news[0], chosen_news[1]

        coin_news.config(text = f"뉴스 속보 : {content} ({int(change_rate * 100)}%)")
        
        global_coin.price = int(global_coin.price * (1 + change_rate))
        global_coin.update_status()

        price_history.append(global_coin.price)

def turn_pass() :
    global_day.next_day()
    my_news.next_day_news()
    refresh_ui()
    draw_chart()


global_coin = Coin()
global_day = Day()
my_asset = Asset()
my_news = News()



window = Tk()
window.title("인생역전 코인 시뮬레이터")
window.geometry("800x600")



title = Label(window, text = "🪙코인 거래소🪙", font=("맑은 고딕", 16, "bold"))
title.pack(side = TOP, pady=10)



asset_label = Label(window, text="", font=("맑은 고딕", 14))
asset_label.pack(pady=5)


chart_canvas = Canvas(window, width=450, height=150, bg="white", relief="sunken", bd=2)
chart_canvas.pack(pady=10)


coin_chart = Label(window, text="실시간 코인 차트", font=("맑은 고딕", 14), bg="#e6e6e6", width=40, height=2)
coin_chart.pack(pady=10)
coin_news = Label(window, text="코인 뉴스", font=("맑은 고딕", 10), wraplength=400)
coin_news.pack(pady=10)



top_frame = Frame(window)
top_frame.pack(pady=10)

button_buy = Button(top_frame, text = "매수", fg = "red", font=("맑은 고딕", 12, "bold"), command = my_asset.buy)
button_sell = Button(top_frame, text = "매도", fg = "blue", font=("맑은 고딕", 12, "bold"), command = my_asset.sell)
button_next_day = Button(top_frame, text = "넘기기", font=("맑은 고딕", 12, "bold"), command = turn_pass)
button_quit = Button(top_frame, text = "게임 종료", font=("맑은 고딕", 12, "bold"), command = quit)

button_buy.grid(row=0, column=0, padx=20)
button_sell.grid(row=0, column=1, padx=20)
button_next_day.grid(row=0,column=2, padx=20)
button_quit.grid(row=1, column=1, pady=30)

refresh_ui()
window.mainloop()
