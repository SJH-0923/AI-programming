# =====================================================
# 연습문제 10 (중급·해양학): 두 지점 거리·방위 계산기
# -----------------------------------------------------
# 목표:
#   위도/경도로 표현된 두 지점 사이의 대권거리(great-circle distance)와
#   초기 방위각(bearing)을 Haversine 공식으로 계산하는 GeoPoint 클래스를 작성.
#   해양 관측 정점 사이 거리, 항해 거리 계산 등에 쓰인다.
#
# Haversine (지구 반지름 R = 6371 km):
#   Δφ = φ2 − φ1,  Δλ = λ2 − λ1   (라디안)
#   a = sin²(Δφ/2) + cosφ1·cosφ2·sin²(Δλ/2)
#   c = 2·atan2(√a, √(1−a))
#   distance = R·c
#
# 초기 방위각(정북 기준 시계방향, 0~360°):
#   y = sinΔλ·cosφ2
#   x = cosφ1·sinφ2 − sinφ1·cosφ2·cosΔλ
#   bearing = (degrees(atan2(y, x)) + 360) mod 360
#
# 주의(오류 가능 지점):
#   - 위경도는 도(degree) 단위 입력 → 삼각함수 전에 math.radians() 로 변환 필수.
#   - atan2(y, x) 의 인자 순서 (y 가 먼저) 를 헷갈리지 말 것.
#   - 음수 경도(서경), 음수 위도(남위) 도 그대로 처리되어야 한다.
#   - 검증값: 부산(35.18,129.08) → 제주(33.51,126.53) ≈ 298.8 km
# =====================================================

from tkinter import *
from tkinter import messagebox
import math

R_EARTH = 6371.0   # km


## 클래스 선언 부분 ##
class GeoPoint:
    """위도(lat)·경도(lon) 한 지점"""

    def __init__(self, lat, lon, name=""):
        self.lat = lat
        self.lon = lon
        self.name = name

    def distance_to(self, other):
        """other 까지의 대권거리 [km]"""
        # TODO: Haversine 공식으로 거리 계산 후 반환
        phi1 = math.radians(self.lat)
        phi2 = math.radians(other.lat)
        dphi = math.radians(other.lat - self.lat)
        dlamb = math.radians(other.lon - self.lon)
        a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlamb / 2)**2
        c = 2 * a * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R_EARTH * c
        
        return distance

    def bearing_to(self, other):
        """other 로 향하는 초기 방위각 [deg, 0~360]"""
        # TODO: 위 방위각 공식으로 계산 후 반환
        phi1 = math.radians(self.lat)
        phi2 = math.radians(other.lat)
        dlamb = math.radians(other.lon - self.lon)
        y = math.sin(dlamb) * math.cos(phi2)
        x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(dlamb)
        bearing = (math.degrees(math.atan2(y, x)) + 360) % 360

        return bearing

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
