import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import urllib.request

class HomePage:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.width = controller.width
        self.height = controller.height

        # None으로 미리 정의
        self.frame = None
        self.nation_listbox_frame = None
        self.flag_frame = None
        self.map_frame = None
        self.scrollbar = None
        self.listbox = None
        self.filter_entry = None
        self.flag_label = None
        self.map_label = None
        self.home_icon = None
        self.search_icon = None
        self.star_icon = None
        self.email_icon = None
        self.home_button = None
        self.search_button = None
        self.favorite_button = None
        self.email_button = None
        self.flag_image = None

        # 실제 Create
        self.create_widgets()

    def create_widgets(self):
        # 첫 번째 페이지 위젯 생성
        self.frame = tk.Frame(self.root, width=self.width, height=self.height)
        self.nation_listbox_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.3), height=int(float(self.height) * 0.8),
                                             bg='lightblue')
        self.flag_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.7), height=int(float(self.height) * 0.4),
                                   bg='lightgray')
        self.map_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.7), height=int(float(self.height) * 0.4),
                                  bg='orange')

        # 리스트 박스와 스크롤 바 생성
        self.scrollbar = tk.Scrollbar(self.nation_listbox_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self.nation_listbox_frame, yscrollcommand=self.scrollbar.set)

        # 나중에 읽어온 국가 명을 여기에 넣음
        for index, country in enumerate(self.controller.complete_country_list):
            self.listbox.insert(tk.END, f"{country['country_name']}")

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.listbox.yview)
        # 리스트 박스 선택 이벤트 바인딩
        self.listbox.bind('<<ListboxSelect>>', self.on_listbox_select)

        # 필터 입력창 생성
        self.filter_entry = ttk.Entry(self.frame)
        # self.filter_entry.insert(0, "국가 이름 필터")
        self.filter_entry.bind('<KeyRelease>', self.on_filter_entry_change)  # 필터 입력창 변경 시 이벤트 바인딩

        # 이미지 자리 표시 레이블 생성
        self.flag_label = tk.Label(self.flag_frame, text="국가 선택 시\n국기 표시\n(이미지)", bg='lightgray')
        self.map_label = tk.Label(self.map_frame, text="국가 선택 시\n지도 정보 표시\n(이미지)", bg='orange')

        self.load_image()

        # 버튼 생성
        self.home_button = ttk.Button(self.frame, image=self.home_icon, command=self.controller.show_home_page)
        self.search_button = ttk.Button(self.frame, image=self.search_icon, command=self.controller.show_search_page)
        self.favorite_button = ttk.Button(self.frame,image=self.star_icon, command=self.controller.show_favorite_page)
        self.email_button = ttk.Button(self.frame, image=self.email_icon, command=self.controller.show_email_page)

        self.place_widgets()

    def load_image(self):
        home_icon = Image.open("Resource/Home_icon.png")
        home_icon = home_icon.resize((60, 60))
        self.home_icon = ImageTk.PhotoImage(home_icon)

        search_icon = Image.open("Resource/Search_icon.png")
        search_icon = search_icon.resize((60, 60))
        self.search_icon = ImageTk.PhotoImage(search_icon)

        star_icon = Image.open("Resource/Star_icon.png")
        star_icon = star_icon.resize((60, 60))
        self.star_icon = ImageTk.PhotoImage(star_icon)

        email_icon = Image.open("Resource/Gmail_icon.png")
        email_icon = email_icon.resize((60, 60))
        self.email_icon = ImageTk.PhotoImage(email_icon)

    def place_widgets(self):
        # 위젯 배치
        self.nation_listbox_frame.place(x=0, y=0, width=int(float(self.width) * 0.3),
                                        height=int(float(self.height) * 0.8))
        self.flag_frame.place(x=int(float(self.width) * 0.3), y=0, width=int(float(self.width) * 0.7),
                              height=int(float(self.height) * 0.4))
        self.map_frame.place(x=int(float(self.width) * 0.3), y=int(float(self.height) * 0.4),
                             width=int(float(self.width) * 0.7), height=int(float(self.height) * 0.4))
        self.filter_entry.place(x=0, y=int(float(self.height) * 0.8), width=int(float(self.width) * 0.3), height=25)

        self.home_button.place(x=0, y=425, width=75, height=75)
        self.search_button.place(x=175, y=425, width=75, height=75)
        self.favorite_button.place(x=250, y=425, width=75, height=75)
        self.email_button.place(x=325, y=425, width=75, height=75)

        # 자리 표시 레이블 프레임에 추가a
        self.flag_label.pack(expand=True)
        self.map_label.pack(expand=True)

    def on_filter_entry_change(self, event):
        filter_text = self.filter_entry.get().lower()
        self.listbox.delete(0, tk.END)
        for country in self.controller.complete_country_list:
            country_name = country['country_name'].lower()
            if filter_text in country_name:
                self.listbox.insert(tk.END, f"{country['country_name']}")

    def on_listbox_select(self, event):
        # 리스트 박스에서 선택된 항목 확인
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            filtered_countries = [country for country in self.controller.complete_country_list
                                  if self.filter_entry.get().lower() in country['country_name'].lower()]
            selected_country = filtered_countries[index]
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

    def show(self):
        self.frame.place(x=0, y=0, width=self.width, height=self.height)

    def hide(self):
        self.frame.place_forget()