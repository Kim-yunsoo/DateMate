import requests
import xml.etree.ElementTree as ET
from tkinter import *
from PIL import ImageTk, Image
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import telepot
from telepot.loop import MessageLoop
import spam

# URL 리스트
urls = [
    #자연관광지
    'https://openapi.gg.go.kr/CTST?KEY=75be4b8be97f4ecaa8fdef12faeba951&pIndex=1&pSize=1000',

    #테마관광지
    'https://openapi.gg.go.kr/TTST?KEY=75be4b8be97f4ecaa8fdef12faeba951&pIndex=1&pSize=1000',

    #체험관광지
    'https://openapi.gg.go.kr/ETST?KEY=75be4b8be97f4ecaa8fdef12faeba951&pIndex=1&pSize=1000'
]

MAP=True
GRAPE=False
FOOD=False
canvas = None
image_label = None
city_name = ""
selected_item = ""

is_city = True

telegram_token = "6076591511:AAHuGtWCzufAn2rLba3WzFKleqD8o8VmXl4"
telegram_chat_id ="5955730862"

bot = telepot.Bot(token=telegram_token)

city = ["수원시", "성남시", "용인시", "안양시", "안산시", "과천시", "광명시", "광주시",
        "군포시", "부천시", "시흥시", "김포시", "안성시", "오산시", "의왕시",
        "이천시", "평택시", "하남시", "화성시", "여주시", "양평군", "고양시",
        "구리시", "남양주시", "동두천시", "양주시", "의정부시", "파주시",
        "포천시", "연평군", "가평군"]

city_num=[0,0,0,0,0,
          0,0,0,0,0,
          0,0,0,0,0,
          0,0,0,0,0,
          0,0,0,0,0,
          0,0,0,0,0,
          0
          ]

def grape_button_clicked():
    global MAP, GRAPE, image_label
    MAP = False
    GRAPE = True
    if GRAPE==True:
        if image_label:
            # image_label.destroy()
            image_label.pack_forget()  # 이미지 라벨 숨기기
        # image_label.configure(image=None)
        display_graph()

def display_graph():
    global city, city_num
    # Tkinter 인터페이스 생성
    # graph_frame = ttk.Frame(midFrame)
    # graph_frame.pack(side=tk.BOTTOM, padx=0, pady=0, fill=tk.BOTH, expand=True)
    # height =0
    # Canvas 생성
    global canvas

    # city_num을 기준으로 상위 5개 도시 선택
    sorted_cities = [c for _, c in sorted(zip(city_num, city), reverse=True)]
    sorted_city_nums = sorted(city_num, reverse=True)
    top_cities = sorted_cities[:5]
    top_city_nums = sorted_city_nums[:5]
    
    canvas.pack(side = "left", fill="both", expand=True)
    canvas.configure(background="white")

    # 그래프 그리기
    bar_width = 50
    bar_spacing = 20
    max_value = max(top_city_nums)
    x_start = 40
    x = x_start
    color_list=['#FFD8D8','#FAECC5','#E4F7BA','#D4F4FA','#DAD9FF']
    for i in range(len(top_cities)):
        height = (top_city_nums[i] / max_value) * (canvas.winfo_height() - 50)
        canvas.create_text(x + bar_width / 2, canvas.winfo_height() - 30, text=top_cities[i], angle=45, anchor='ne')
        canvas.create_rectangle(x, canvas.winfo_height() - height - 20, x + bar_width, canvas.winfo_height() - 30, fill=color_list[i])
        x += bar_width + bar_spacing

    canvas.configure(scrollregion=canvas.bbox("all"))
