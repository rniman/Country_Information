import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
from io import BytesIO
import urllib.request
import requests

class SearchPage:
    MAX_PAGE = 3

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.width = controller.width
        self.height = controller.height

        # 현재 상세 정보 페이지
        self.page = 0

        self.frame = None
        self.flag_frame = None
        self.map_frame = None
        self.text_frame = None
        self.page_button_frame = None

        self.flag_label = None
        self.map_label = None
        self.detail_info_text = None
        self.prev_button = None
        self.next_button = None
        self.home_icon = None
        # self.search_icon = None
        self.star_icon = None
        self.email_icon = None
        self.home_button = None
        self.favorite_button = None
        self.email_button = None
        self.zoom_in_button = None
        self.zoom_out_button = None
        self.selected_country_index = None
        self.zoom = 3
        self.create_widgets()

    def create_widgets(self):
        # 두 번째 페이지 위젯 생성
        self.frame = tk.Frame(self.root, width= self.width, height=self.height)
        self.flag_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.5), height=int(float(self.height) * 0.4),
                                   bg='lightgray')
        self.map_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.5), height=int(float(self.height) * 0.4),
                                  bg='orange')
        self.text_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.5), height=int(float(self.height) * 0.7),
                                  bg='lightblue')
        self.page_button_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.5), height=int(float(self.height) * 0.1),
                                  bg='lightblue')

        self.flag_label = tk.Label(self.flag_frame, text="국가 선택 시\n국기 표시\n(이미지)", bg='lightgray')
        self.map_label = tk.Label(self.map_frame, text="국가 선택 시\n지도 정보 표시\n(이미지)", bg='orange')

        # 글꼴을 바꿔야지 \n같은 문자가 음표로 바뀌는 일이 없음
        self.detail_info_text = tk.Text(self.text_frame, font=("Helvetica", 8))

        self.prev_button = ttk.Button(self.page_button_frame, text="<<", command=self.prev_page)
        self.next_button = ttk.Button(self.page_button_frame, text=">>", command=self.next_page)

        self.load_image()
        self.home_button = ttk.Button(self.frame, image=self.home_icon, command=self.controller.show_home_page)
        self.favorite_button = ttk.Button(self.frame, image=self.star_icon, command=self.controller.show_favorite_page)
        self.email_button = ttk.Button(self.frame,image=self.email_icon, command=self.controller.show_email_page)
        self.zoom_in_button = ttk.Button(self.map_frame, text="+", command=self.zoom_in_map)
        self.zoom_out_button = ttk.Button(self.map_frame, text="-", command=self.zoom_out_map)

        self.place_widgets()

    def load_image(self):
        home_icon = Image.open("Resource/Home_icon.png")
        home_icon = home_icon.resize((60, 60))
        self.home_icon = ImageTk.PhotoImage(home_icon)

        # search_icon = Image.open("Resource/Search_icon.png")
        # search_icon = search_icon.resize((60, 60))
        # self.search_icon = ImageTk.PhotoImage(search_icon)

        star_icon = Image.open("Resource/Star_icon.png")
        star_icon = star_icon.resize((60, 60))
        self.star_icon = ImageTk.PhotoImage(star_icon)

        email_icon = Image.open("Resource/Gmail_icon.png")
        email_icon = email_icon.resize((60, 60))
        self.email_icon = ImageTk.PhotoImage(email_icon)

    def place_widgets(self):
        # 두 번째 페이지 위젯 배치
        self.flag_frame.place(x=0, y=0, width=int(float(self.width) * 0.5), height=int(float(self.height) * 0.4))
        self.map_frame.place(x=0, y=int(float(self.height) * 0.4), width=int(float(self.width) * 0.5),
                             height=int(float(self.height) * 0.4))
        self.text_frame.place(x=int(float(self.width) * 0.5), y=0, width=int(float(self.width) * 0.5),
                              height=int(float(self.height) * 0.7))
        self.page_button_frame.place(x=int(float(self.width) * 0.5), y=int(float(self.height) * 0.7),
                                     width=int(float(self.width) * 0.5), height=int(float(self.height) * 0.1))

        self.detail_info_text.place(x=0, y=0, width=int(float(self.width) * 0.5), height=int(float(self.height) * 0.7))
        self.flag_label.pack(expand=True)
        self.map_label.pack(expand=True)

        self.prev_button.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        self.next_button.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)

        self.home_button.place(x=0, y=425, width=75, height=75)
        self.favorite_button.place(x=250, y=425, width=75, height=75)
        self.email_button.place(x=325, y=425, width=75, height=75)

        self.zoom_in_button.place(x=int(float(self.width) * 0.5) - 20, y=int(float(self.height) * 0.4) - 20,
                               width=20, height=20)
        self.zoom_out_button.place(x=0, y=int(float(self.height) * 0.4) - 20,
                               width=20, height=20)

    def prev_page(self):
        self.page -= 1
        if self.page < 0:
            self.page = SearchPage.MAX_PAGE - 1
        self.display_selected_info()

    def next_page(self):
        self.page += 1
        if self.page >= SearchPage.MAX_PAGE:
            self.page = 0
        self.display_selected_info()

    def display_selected_flag(self):
        selected_country = self.controller.complete_country_list[self.selected_country_index]
        url = selected_country['country_img_url']
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))

        # 이미지 리사이즈
        flag_width = self.flag_frame.winfo_width()
        flag_height = self.flag_frame.winfo_height()
        im = im.resize((flag_width, flag_height))

        self.flag_image = ImageTk.PhotoImage(im)
        self.flag_label.config(image=self.flag_image)
        self.flag_label.image = self.flag_image  # 참조 유지

    def display_selected_map(self):
        selected_country = self.controller.complete_country_list[self.selected_country_index]
        # gu_name = selected_country['country_name']
        gu_name = selected_country['country_eng_name']
        gu_center = self.controller.gmaps.geocode(f"{gu_name}")[0]['geometry']['location']
        gu_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={gu_center['lat']}," \
                     f"{gu_center['lng']}&zoom={self.zoom }&size=400x400&maptype=roadmap"

        lat, lng = float(gu_center['lat']), float(gu_center['lng'])
        marker_url = f"&markers=color:red%7C{lat},{lng}"
        gu_map_url += marker_url

        response = requests.get(gu_map_url + '&key=' + self.controller.Google_API_Key)
        if response.status_code == 200:
            try:
                image = Image.open(io.BytesIO(response.content))
                photo = ImageTk.PhotoImage(image)
                self.map_label.configure(image=photo)
                self.map_label.image = photo
            except IOError as e:
                print("Error: Unable to open image. Details:", e)
        else:
            print("Error: Unable to fetch image. Status code:", response.status_code)

    def zoom_in_map(self):
        if self.zoom < 10:
            self.zoom += 1
        self.display_selected_map()

    def zoom_out_map(self):
        if self.zoom > 2:
            self.zoom -= 1
        self.display_selected_map()

    def display_selected_info(self):
        self.detail_info_text.config(state='normal')
        self.detail_info_text.delete("1.0", tk.END)
        selected_country = self.controller.complete_country_list[self.selected_country_index]
        if self.page == 0:  # 기본 정보
            self.detail_info_text.insert(tk.END, "[외교부 국가별 기본정보(1/3)]\n\n")
            self.detail_info_text.insert(tk.END, "선택 국가: {0}\n".format(selected_country['country_name']))
            self.detail_info_text.insert(tk.END, "인구수: {0}명\n".format(selected_country['population']))
            self.detail_info_text.insert(tk.END, "면적: {0}km^2\n\n".format(selected_country['area']))
            self.detail_info_text.insert(tk.END, selected_country['country_basic'])
        elif self.page == 1:  # 사건 사고
            self.detail_info_text.insert(tk.END, "[외교부 사고 정보(2/3)]\n\n")
            self.detail_info_text.insert(tk.END, selected_country['accident_info'])
        else:
            self.detail_info_text.insert(tk.END, "[외교부 여행 경보(3/3)]\n\n")
            self.detail_info_text.insert(tk.END, selected_country['warning_info'])
        self.detail_info_text.config(state='disabled')

    def show(self):
        self.frame.place(x=0, y=0, width=400, height=self.height)
        self.display_selected_flag()
        self.display_selected_map()
        self.page = 0
        self.display_selected_info()

    def hide(self):
        self.frame.place_forget()