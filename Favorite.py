import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class FavoritePage:
    MAX_PAGE = 2

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.width = controller.width
        self.height = controller.height

        self.frame = None
        self.graph_frame = None
        self.graph_canvas = None
        self.graph_scrollbar = None
        self.graph_page = 0
        self.graph_title_label = None
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
        self.favorite_list = None

        self.create_widgets()

    def create_widgets(self):
        # 두 번째 페이지 위젯 생성
        self.frame = tk.Frame(self.root, width=self.width, height=self.height)
        self.graph_frame = tk.Frame(self.frame, width=self.width, height=int(float(self.height) * 0.6), bg='white')
        self.graph_scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.graph_canvas = tk.Canvas(self.graph_frame, width=self.width, height=int(float(self.height) * 0.6)
                                      , xscrollcommand=self.graph_scrollbar.set)

        self.graph_title_label = tk.Label(self.graph_frame, text="", anchor='center')
        self.graph_label = tk.Label(self.frame, text="", bg='lightgray', anchor='center')

        self.prev_button = ttk.Button(self.frame, text="<<", command=self.on_prev_graph)
        self.next_button = ttk.Button(self.frame, text=">>", command=self.on_next_graph)

        self.load_image()

        self.home_button = ttk.Button(self.frame, image=self.home_icon, command=self.controller.show_home_page)
        # 관심국가에서 해당 버튼은 관심국가 해제를 하는 것
        self.favorite_button = ttk.Button(self.frame, image=self.star_icon, command=self.controller.release_favorite_page)
        self.email_button = ttk.Button(self.frame, image=self.email_icon, command=self.controller.show_email_page)

        self.place_widgets()

    def load_image(self):
        home_icon = Image.open("Resource/Home_icon.png")
        home_icon = home_icon.resize((60, 60))
        self.home_icon = ImageTk.PhotoImage(home_icon)

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
        self.graph_canvas.place(x=0, y=0, width=self.width, height=int(float(self.height) * 0.6))
        self.graph_scrollbar.place(x=0, y=int(float(self.height) * 0.6), width=self.width, height=20)
        self.graph_scrollbar.config(command=self.graph_canvas.xview)
        self.graph_canvas.config(scrollregion=self.graph_canvas.bbox(tk.ALL))

        self.graph_title_label.place(x=0, y=0, width=self.width, height=20)
        self.graph_label.place(x=0, y=325, width=self.width, height=50)

        self.prev_button.place(x=150, y=375, width=50, height=50)
        self.next_button.place(x=200, y=375, width=50, height=50)

        self.home_button.place(x=0, y=425, width=75, height=75)
        self.favorite_button.place(x=250, y=425, width=75, height=75)
        self.email_button.place(x=325, y=425, width=75, height=75)

    def on_prev_graph(self):
        self.graph_page -= 1
        if self.graph_page < 0:
            self.graph_page = FavoritePage.MAX_PAGE - 1
        self.display_graph()

    def on_next_graph(self):
        self.graph_page += 1
        if self.graph_page >= FavoritePage.MAX_PAGE:
            self.graph_page = 0
        self.display_graph()

    def wrap_text(self, text, line_length=4):
        wrapped_lines = []
        for i in range(0, len(text), line_length):
            wrapped_lines.append(text[i:i + line_length])
        return "\n".join(wrapped_lines[:3])

    def display_graph(self):
        self.graph_canvas.delete("all")  # 기존 그래프를 지우기
        c_width = int(self.graph_canvas['width'])
        c_height = int(self.graph_canvas['height'])

        width_offset = 50
        graph_width = 30
        graph_top_padding = 20
        graph_bottom_padding = 50
        favorite_num = len(self.favorite_list)

        if self.graph_page == 0:  # 인구수
            # 최대 인구와 해당 국가 이름을 동시에 계산
            max_population_country = max(self.favorite_list, key=lambda country: float(country['population']))
            max_population = float(max_population_country['population'])
            max_country_name = max_population_country['country_name']

            min_population_country = min(self.favorite_list, key=lambda country: float(country['population']))
            min_population = float(min_population_country['population'])
            min_country_name = min_population_country['country_name']

            self.graph_title_label.config(text='<인구 수 그래프>')
            self.graph_label.config(text='최다 인구 국가:{0} - {1}명\n최소 인구 국가:{2} - {3}명'.format(
                max_country_name, max_population, min_country_name, min_population))
        elif self.graph_page == 1:  # 면적
            max_area_country = max(self.favorite_list, key=lambda country: float(country['area']))
            max_area = float(max_area_country['area'])
            max_country_name = max_area_country['country_name']

            min_area_country = min(self.favorite_list, key=lambda country: float(country['area']))
            min_area = float(min_area_country['area'])
            min_area_name = min_area_country['country_name']

            self.graph_title_label.config(text='<영토 면적 그래프>')
            self.graph_label.config(text='최대 면적 국가:{0} - {1}km^2\n최소 면적 국가:{2} - {3}km^2'.format(
                max_country_name, max_area, min_area_name, min_area))

        for index, country in enumerate(self.favorite_list):
            if self.graph_page == 0:  # 인구수
                y1 = graph_top_padding + (c_height - graph_bottom_padding - graph_top_padding) * \
                     (1 - float(country['population']) / max_population)
                text_color = 'skyblue'
            elif self.graph_page == 1:  # 면적
                y1 = graph_top_padding + (c_height - graph_bottom_padding - graph_top_padding) * \
                     (1 - float(country['area']) / max_area)
                text_color = 'orange'

            self.graph_canvas.create_rectangle(width_offset * index + width_offset / 2 - graph_width/2,
                                               y1,
                                               width_offset * index + width_offset / 2 + graph_width/2,
                                               c_height - graph_bottom_padding,
                                               fill=text_color)
            wrapped_text = self.wrap_text(country['country_name'])
            self.graph_canvas.create_text(width_offset * index + width_offset / 2, c_height - 25, text=wrapped_text)

        self.graph_canvas.config(scrollregion=(0, 0, width_offset * favorite_num + width_offset, c_height))

    def show(self):
        self.favorite_list = []
        self.frame.place(x=0, y=0, width=self.width, height=self.height)
        for index, country in enumerate(self.controller.complete_country_list):
            if country['country_id'] in self.controller.favorite_list:
                self.favorite_list.append(country)
        self.display_graph()

    def hide(self):
        self.frame.place_forget()