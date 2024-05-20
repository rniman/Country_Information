import tkinter as tk
from tkinter import ttk

class FavoritePage:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.width = controller.width
        self.height = controller.height

        self.create_widgets()

    def create_widgets(self):
        # 두 번째 페이지 위젯 생성
        self.frame = tk.Frame(self.root, width=self.width, height=self.height)
        self.graph_frame = tk.Frame(self.frame, width=self.width, height=int(float(self.height) * 0.6), bg='lightgray')
        self.graph_label= tk.Label(self.graph_frame, text="관심 국가\n비교 그래프 표시", bg='white')

        self.prev_button = ttk.Button(self.frame, text="<<")
        self.next_button = ttk.Button(self.frame, text=">>")

        self.home_button = ttk.Button(self.frame, text="Home", command=self.controller.show_home_page)

        # 관심국가에서 해당 버튼은 관심국가 해제를 하는 것
        self.favorite_button = ttk.Button(self.frame, text="Favorite", command=self.controller.show_favorite_page)
        self.email_button = ttk.Button(self.frame, text="Email", command=self.controller.show_email_page)

        self.place_widgets()

    def place_widgets(self):
        # 두 번째 페이지 위젯 배치
        self.graph_frame.place(x=0, y=0, width=self.width, height=int(float(self.height) * 0.6))
        self.graph_frame.pack(expand=True, fill=tk.BOTH)
        self.graph_label.place(x=0, y=0, width=self.width, height=int(float(self.height) * 0.6))

        self.prev_button.place(x=150, y=425, width=50, height=50)
        self.next_button.place(x=200, y=425, width=50, height=50)

        self.home_button.place(x=0, y=425, width=75, height=75)
        self.favorite_button.place(x=250, y=425, width=75, height=75)
        self.email_button.place(x=325, y=425, width=75, height=75)

    def show(self):
        self.frame.place(x=0, y=0, width=self.width, height=self.height)

    def hide(self):
        self.frame.place_forget()