import tkinter as tk
from tkinter import ttk

class SearchPage:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.width = controller.width
        self.height = controller.height

        self.create_widgets()

    def create_widgets(self):
        # 두 번째 페이지 위젯 생성
        self.frame = tk.Frame(self.root, width= self.width, height=self.height)
        self.flag_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.5), height=int(float(self.height) * 0.4),
                                   bg='lightgray')
        self.map_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.5), height=int(float(self.height) * 0.4),
                                  bg='orange')
        self.flag_label = tk.Label(self.flag_frame, text="국가 선택 시\n국기 표시\n(이미지)", bg='lightgray')
        self.map_label = tk.Label(self.map_frame, text="국가 선택 시\n지도 정보 표시\n(이미지)", bg='orange')

        self.detail_info_label = tk.Label(self.frame, text="국가 상세 정보 표시", bg='lightblue')

        self.prev_button = ttk.Button(self.frame, text="<<")
        self.next_button = ttk.Button(self.frame, text=">>")

        self.home_button = ttk.Button(self.frame, text="Home", command=self.controller.show_home_page)
        self.favorite_button = ttk.Button(self.frame, text="Favorite", command=self.controller.show_favorite_page)
        self.email_button = ttk.Button(self.frame, text="Email", command=self.controller.show_email_page)

        self.place_widgets()

    def place_widgets(self):
        # 두 번째 페이지 위젯 배치
        self.flag_frame.place(x=0, y=0, width=int(float(self.width) * 0.5), height=int(float(self.height) * 0.4))
        self.map_frame.place(x=0, y=int(float(self.height) * 0.4), width=int(float(self.width) * 0.5),
                             height=int(float(self.height) * 0.4))
        self.detail_info_label.place(x=int(float(self.width) * 0.5), y=0, width=int(float(self.width) * 0.5),
                                     height=int(float(self.height) * 0.8))
        self.flag_label.pack(expand=True)
        self.map_label.pack(expand=True)

        self.prev_button.place(x=150, y=425, width=50, height=50)
        self.next_button.place(x=200, y=425, width=50, height=50)
        self.home_button.place(x=0, y=425, width=75, height=75)
        self.favorite_button.place(x=250, y=425, width=75, height=75)
        self.email_button.place(x=325, y=425, width=75, height=75)

    def show(self):
        self.frame.place(x=0, y=0, width=400, height=self.height)

    def hide(self):
        self.frame.place_forget()