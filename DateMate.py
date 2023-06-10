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

