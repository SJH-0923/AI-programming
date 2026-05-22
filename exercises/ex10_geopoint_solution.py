# =====================================================
# 연습문제 10 (중급·해양학) - 정답: 두 지점 거리·방위 계산기 (Haversine)
# =====================================================
from tkinter import *
from tkinter import messagebox
import math

R_EARTH = 6371.0   # km


## 클래스 선언 부분 ##
class GeoPoint:
    def __init__(self, lat, lon, name=""):
        self.lat = lat
        self.lon = lon
        self.name = name

    def distance_to(self, other):
        phi1 = math.radians(self.lat)
        phi2 = math.radians(other.lat)
        dphi = math.radians(other.lat - self.lat)
        dlmb = math.radians(other.lon - self.lon)
        a = (math.sin(dphi / 2) ** 2
             + math.cos(phi1) * math.cos(phi2) * math.sin(dlmb / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R_EARTH * c

    def bearing_to(self, other):
        phi1 = math.radians(self.lat)
        phi2 = math.radians(other.lat)
        dlmb = math.radians(other.lon - self.lon)
        y = math.sin(dlmb) * math.cos(phi2)
        x = (math.cos(phi1) * math.sin(phi2)
             - math.sin(phi1) * math.cos(phi2) * math.cos(dlmb))
        return (math.degrees(math.atan2(y, x)) + 360) % 360

    def __repr__(self):
        return f"GeoPoint({self.lat}, {self.lon}, {self.name!r})"


## 함수 선언 부분 ##
def on_calc():
    try:
        p1 = GeoPoint(float(e_lat1.get()), float(e_lon1.get()), "지점1")
        p2 = GeoPoint(float(e_lat2.get()), float(e_lon2.get()), "지점2")
    except ValueError:
        messagebox.showerror("입력 오류", "위도/경도는 숫자로 입력해 주세요.")
        return

    d = p1.distance_to(p2)
    b = p1.bearing_to(p2)
    result.config(text=f"거리   = {d:9.3f} km\n방위각 = {b:9.2f}°  (정북 기준)")


## 메인 코드 부분 ##
window = Tk()
window.title("연습 10 - 거리·방위 계산기 (Haversine)")
window.geometry("420x240")

Label(window, text="지점 1", font=("맑은 고딕", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 2))
Label(window, text="위도:").grid(row=1, column=0, sticky="e", padx=5)
e_lat1 = Entry(window, width=10); e_lat1.grid(row=1, column=1); e_lat1.insert(0, "35.18")
Label(window, text="경도:").grid(row=2, column=0, sticky="e", padx=5)
e_lon1 = Entry(window, width=10); e_lon1.grid(row=2, column=1); e_lon1.insert(0, "129.08")

Label(window, text="지점 2", font=("맑은 고딕", 10, "bold")).grid(row=0, column=2, columnspan=2, pady=(10, 2))
Label(window, text="위도:").grid(row=1, column=2, sticky="e", padx=5)
e_lat2 = Entry(window, width=10); e_lat2.grid(row=1, column=3); e_lat2.insert(0, "33.51")
Label(window, text="경도:").grid(row=2, column=2, sticky="e", padx=5)
e_lon2 = Entry(window, width=10); e_lon2.grid(row=2, column=3); e_lon2.insert(0, "126.53")

Button(window, text="계산", width=14, command=on_calc).grid(row=3, column=0, columnspan=4, pady=12)
result = Label(window, text="", font=("Consolas", 12), justify=LEFT)
result.grid(row=4, column=0, columnspan=4)

window.mainloop()
