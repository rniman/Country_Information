import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class FavoritePage:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.width = controller.width
        self.height = controller.height

        self.frame = None
        self.graph_frame = None
        self.graph_label = None
        self.prev_button = None
        self.next_button = None
        self.home_icon = None
        # self.search_icon = None
        self.star_icon = None
        self.email_icon = None
        self.home_button = None
        self.favorite_button = None
        self.email_button = None

        self.create_widgets()

    def create_widgets(self):
        # 두 번째 페이지 위젯 생성
        self.frame = tk.Frame(self.root, width=self.width, height=self.height)
        self.graph_frame = tk.Frame(self.frame, width=self.width, height=int(float(self.height) * 0.6), bg='white')
        self.graph_label= tk.Label(self.graph_frame, text="관심 국가\n비교 그래프 표시", bg='lightgray')

        self.prev_button = ttk.Button(self.frame, text="<<")
        self.next_button = ttk.Button(self.frame, text=">>")

        self.load_image()

        self.home_button = ttk.Button(self.frame, image=self.home_icon, command=self.controller.show_home_page)
        # 관심국가에서 해당 버튼은 관심국가 해제를 하는 것
        self.favorite_button = ttk.Button(self.frame, image=self.star_icon, command=self.controller.show_favorite_page)
        self.email_button = ttk.Button(self.frame, image=self.email_icon, command=self.controller.show_email_page)

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
        self.graph_frame.place(x=0, y=0, width=self.width, height=int(float(self.height) * 0.6))
        self.graph_frame.pack(expand=True, fill=tk.BOTH)
        self.graph_label.place(x=0, y=0, width=self.width, height=int(float(self.height) * 0.6))

        self.prev_button.place(x=150, y=325, width=50, height=50)
        self.next_button.place(x=200, y=325, width=50, height=50)

        self.home_button.place(x=0, y=425, width=75, height=75)
        self.favorite_button.place(x=250, y=425, width=75, height=75)
        self.email_button.place(x=325, y=425, width=75, height=75)

    def show(self):
        self.frame.place(x=0, y=0, width=self.width, height=self.height)

    def hide(self):
        self.frame.place_forget()