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
