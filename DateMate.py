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


def search_tourism_location():
    # Google Maps API 요청을 위한 API 키 설정
    api_key = 'AIzaSyApjfiZq66Iv1zilLZBdYPrFRsJqLEAbXM'  # 사용자 고유의 API 키로 변경해야 합니다.

    # 검색어 가져오기
    keyword = selected_item

    # API 요청 URL 생성
    url = f'https://maps.googleapis.com/maps/api/staticmap?center={keyword}&zoom={zoom}&size=800x600&markers=color:red%7C{keyword}&key={api_key}'

    # API 요청 보내기
    response = requests.get(url)

    try:
        # 이미지 데이터 받기
        image_data = response.content

        # 이미지 열기
        image = Image.open(BytesIO(image_data))

        # 이미지 크기 조정
        image = image.resize((420, 245), Image.ANTIALIAS)

        # 이미지를 tkinter에서 표시할 수 있는 형식으로 변환
        photo = ImageTk.PhotoImage(image)

        global canvas
        if (canvas):
            canvas.pack_forget()

        # 이미지 라벨 생성 및 표시
        image_label.configure(image=photo)
        image_label.image = photo

    except Exception as e:
        print(f'Error: {e}')


def select_item(event):
    global MAP, GRAPE
    global selected_item
    global canvas

    MAP=True
    GRAPE=False
    # Get the selected item from the info_listbox
    selected_index = info_listbox.curselection()
    if selected_index and MAP==True:
        if canvas:
            canvas.delete("all")
        image_label.pack(side="left", padx=0, pady=0, anchor="nw")
        selected_item = info_listbox.get(selected_index)
        search_tourism_location()  # 선택된 항목에 대한 지도 보기 함수 호출


def search():
    global city_name, is_city

    # keyword =entry.get()  # 검색어 입력란에서 키워드 가져오기
    result = spam.strlen(entry.get())
    keyword =result  # 검색어 입력란에서 키워드 가져오기

    # keyword=userInput
    if keyword in city:
        is_city = True
        city_name = keyword
    else:
        is_city = False
    update_listbox()

def update_listbox():
    global urls
    info_listbox.delete(0, END)  # 기존 아이템 모두 삭제
    for url in urls:
        xml_data = fetch_data(url)
        if xml_data:
            data = parse_data(xml_data)
            if data:
                for info in data:
                    if FOOD:
                        #info_listbox.insert(END, f"{info['RESTRT_NM']}")
                        if city_name == "" and is_city:
                            info_listbox.insert(END, f"{info['RESTRT_NM']}")
                            for name in city:
                                if name in info['REFINE_ROADNM_ADDR']:
                                    city_num[city.index(name)] += 1
                        elif city_name != "" and is_city:
                            if city_name in info['REFINE_ROADNM_ADDR']:
                                info_listbox.insert(END, f"{info['RESTRT_NM']}")
                    else:
                        if city_name == "" and is_city:
                            info_listbox.insert(END, f"{info['TURSM_INFO_NM']}")
                            for name in city:
                                if name in info['SM_RE_ADDR']:
                                    city_num[city.index(name)] += 1
                        elif city_name != "" and is_city:
                            if city_name in info['SM_RE_ADDR']:
                                info_listbox.insert(END, f"{info['TURSM_INFO_NM']}")


def food_button_clicked():
    global urls, FOOD
    FOOD = True
    # 새로운 XML 데이터를 가져오기 위해 URL을 업데이트
    urls = [
        # 음식점 데이터
        'https://openapi.gg.go.kr/PlaceThatDoATasteyFoodSt?KEY=75be4b8be97f4ecaa8fdef12faeba951&pIndex=1&pSize=1000'
    ]

    #selected_item = ""  # 선택된 항목 초기화
    update_listbox()  # 리스트박스 업데이트
    #search_tourism_location()  # 지도 보기 업데이트

def spot_button_clicked():
    global urls, FOOD
    FOOD = False
    # 새로운 XML 데이터를 가져오기 위해 URL을 업데이트
    urls = [
          #자연관광지
    'https://openapi.gg.go.kr/CTST?KEY=75be4b8be97f4ecaa8fdef12faeba951&pIndex=1&pSize=1000',

    #테마관광지
    'https://openapi.gg.go.kr/TTST?KEY=75be4b8be97f4ecaa8fdef12faeba951&pIndex=1&pSize=1000',

    #체험관광지
    'https://openapi.gg.go.kr/ETST?KEY=75be4b8be97f4ecaa8fdef12faeba951&pIndex=1&pSize=1000'
    ]

    #selected_item = ""  # 선택된 항목 초기화
    update_listbox()  # 리스트박스 업데이트
    #search_tourism_location()  # 지도 보기 업데이트


def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.HTTPError as e:
        print(f'HTTP 오류 발생: {e}')
        return None

def zoom_in():
    global zoom
    zoom += 1
    search_tourism_location()

def zoom_out():
    global zoom
    if zoom > 1:
        zoom -= 1
    search_tourism_location()

def parse_data(xml_data):
    try:
        root = ET.fromstring(xml_data)
        rows = root.findall('.//row')
        data = []
        for row in rows:
            tursm_info_nm_element = row.find('TURSM_INFO_NM')
            restrt_info_nm_element = row.find('RESTRT_NM')
            if restrt_info_nm_element is not None and restrt_info_nm_element.text is not None:
                info = {
                    'RESTRT_NM': restrt_info_nm_element.text,
                    'REFINE_ROADNM_ADDR': row.find('REFINE_ROADNM_ADDR').text,
                }
                data.append(info)
            elif tursm_info_nm_element is not None and tursm_info_nm_element.text is not None:
                info = {
                    'TURSM_INFO_NM': tursm_info_nm_element.text,
                    'SM_RE_ADDR': row.find('SM_RE_ADDR').text,
                    'TELNO': row.find('TELNO').text if row.find('TELNO') is not None else ''
                }
                data.append(info)
        return data  # 리스트 형태로 데이터 반환
    except (ValueError, ET.ParseError) as e:
        print(f'XML 파싱 오류 발생: {e}')
        return []  # 빈 리스트 반환
    

def telegram_button_clicked():
    bot.sendMessage(telegram_chat_id, text='안녕하세요! DataMate입니다. 도시명을 입력해주세요 :)')
    
    def handle_message(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        
        if content_type == 'text':
            command = msg['text']
            city_name = command.strip()
            send_tourism_locations(chat_id, city_name)
            send_food_locations(chat_id, city_name)

    def send_tourism_locations(chat_id, city_name):
        locations = []

        # 관광지 정보 가져오기
        for url in urls[:3]:
            xml_data = fetch_data(url)
            if xml_data:
                data = parse_data(xml_data)
                if data:
                    for info in data:
                        if city_name in info.get('SM_RE_ADDR', '') or city_name in info.get('REFINE_ROADNM_ADDR', ''):
                            if 'TURSM_INFO_NM' in info:
                                locations.append(info['TURSM_INFO_NM'])
                            elif 'RESTRT_NM' in info:
                                locations.append(info['RESTRT_NM'])

        # 관광지 정보 전송
        if locations:
            message = f"{city_name}에 있는 관광지 정보:\n"
            for location in locations:
                message += f"- {location}\n"

            bot.sendMessage(chat_id=chat_id, text=message)
        else:
            bot.sendMessage(chat_id=chat_id, text=f"{city_name}에 대한 관광지 정보를 찾을 수 없습니다.")

    def send_food_locations(chat_id, city_name):
        locations = []

        # 맛집 정보 가져오기
        url = 'https://openapi.gg.go.kr/PlaceThatDoATasteyFoodSt?KEY=75be4b8be97f4ecaa8fdef12faeba951&pIndex=1&pSize=1000'
        xml_data = fetch_data(url)
        if xml_data:
            data = parse_data(xml_data)
            if data:
                for info in data:
                    if city_name in info.get('SM_RE_ADDR', '') or city_name in info.get('REFINE_ROADNM_ADDR', ''):
                        locations.append(info['RESTRT_NM'])

        # 맛집 정보 전송
        if locations:
            message = f"{city_name}에 있는 맛집 정보:\n"
            for location in locations:
                message += f"- {location}\n"

            bot.sendMessage(chat_id=chat_id, text=message)
        else:
            bot.sendMessage(chat_id=chat_id, text=f"{city_name}에 대한 맛집 정보를 찾을 수 없습니다.")

    MessageLoop(bot, handle_message).run_as_thread()

root = Tk()
root.geometry("740x400")  # 가로 800, 세로 400 크기로 설정
root.title("Date Mate")
root.configure(background="#D9E5FF")

# 상단 프레임
topFrame = Frame(root)
topFrame.pack(fill="both", side="top")
topFrame.configure(background="#D9E5FF")

# 중간 프레임
midFrame = Frame(root, width=200)
midFrame.pack(fill="x", side="top")
midFrame.configure(background="#D9E5FF")



# 검색 입력란
search_label = Label(topFrame, text="경기도 시 검색 ")
search_label.pack(side="left", padx=0, pady=10, anchor="nw")  # 왼쪽 상단 정렬
entry = Entry(topFrame, width=30)  # 너비를 50으로 설정
entry.pack(side="left", padx=0, pady=10, anchor="nw")  # 왼쪽 상단 정렬

# 검색 버튼
image = Image.open("검색.png")
image = image.resize((15, 15), Image.ANTIALIAS)
photo_search = ImageTk.PhotoImage(image)

search_button = Button(topFrame,image=photo_search, width=17, height=17, command=search)
search_button.pack(side="left", padx=0, pady=7, anchor="nw")  # 왼쪽 상단 정렬

image = Image.open("그래프.png")
image = image.resize((70, 70), Image.ANTIALIAS)
photo_grape = ImageTk.PhotoImage(image)

# 막대그래프 UI
grape_button = Button(root,  image=photo_grape, width=80, height=80, command=grape_button_clicked, bg="white",borderwidth=5)
grape_button.pack(side="right", padx=10, pady=10, anchor="nw")  # 오른쪽 하단 정렬

image = Image.open("텔레그램.png")
image = image.resize((70, 70), Image.ANTIALIAS)
photo_tele = ImageTk.PhotoImage(image)

# 텔레그램 UI


Tele_button = Button(root, image=photo_tele, width=80, height=80, bg="white",borderwidth=5, command=telegram_button_clicked)
Tele_button.pack(side="right", padx=10, pady=10, anchor="nw")  # 왼쪽 상단 정렬

image = Image.open("맛집.png")
image = image.resize((70, 70), Image.ANTIALIAS)
photo_Food = ImageTk.PhotoImage(image)

# 맛집리스트 UI
Food_button = Button(root, image=photo_Food, width=80, height=80, bg="white",borderwidth=5, command=food_button_clicked)
Food_button.pack(side="right", padx=10, pady=10, anchor="nw")  # 왼쪽 상단 정렬

image = Image.open("관광지.png")
image = image.resize((70, 70), Image.ANTIALIAS)
photo_Spot = ImageTk.PhotoImage(image)

# 장소리스트 UI
Spot_button = Button(root, image=photo_Spot, width=80, height=80, bg="white",borderwidth=5, command=spot_button_clicked)
Spot_button.pack(side="right", padx=10, pady=10, anchor="nw")  # 왼쪽 상단 정렬



# 리스트 박스 생성
info_listbox = Listbox(midFrame, width=40, height=15)
info_listbox.pack(side="left", padx=5, pady=0, anchor="nw")  # 상단 정렬

# 스크롤바 생성
scrollbar = Scrollbar(midFrame)
scrollbar.pack(side="left", fill=Y)

# 스크롤바와 리스트 박스 연결
scrollbar.config(command=info_listbox.yview)

canvas = Canvas(midFrame,width=50, height=15)
canvas.pack(side = "left", fill="both", expand=True)
canvas.configure(background="white")



# 이미지 라벨 생성
image_label = Label(midFrame)
#image_label = Listbox(midFrame, width=50, height=15)
image_label.pack(side="left", padx=0, pady=0, anchor="nw")

image = Image.open("줌인.png")
image = image.resize((35, 35), Image.ANTIALIAS)
photo_in = ImageTk.PhotoImage(image)


zoom_in_button = Button(topFrame, image=photo_in, command=zoom_in, bg="#EBF7FF")
zoom_in_button.pack(side="right", padx=5, pady=3, anchor="nw")

image = Image.open("줌아웃.png")
image = image.resize((35, 35), Image.ANTIALIAS)
photo_out = ImageTk.PhotoImage(image)

zoom_out_button = Button(topFrame, image=photo_out, command=zoom_out, bg="#EBF7FF")
zoom_out_button.pack(side="right", padx=5, pady=3, anchor="nw")
      

info_listbox.bind('<<ListboxSelect>>', select_item)
zoom = 15
update_listbox()
root.mainloop()