import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class EmailPage:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.width = controller.width
        self.height = controller.height

        self.frame = None
        self.favorite_nation_listbox_frame = None
        self.favorite_nation_info_frame = None
        self.user_message_frame = None
        self.home_icon = None
        self.email_icon = None
        self.home_button = None
        self.email_address_entry = None
        self.email_button = None
        self.listbox_scrollbar = None
        self.listbox = None
        self.info_scrollbar = None
        self.info_text = None
        self.user_message_scrollbar = None
        self.message_text = None

        self.create_widgets()

    def create_widgets(self):
        # 두 번째 페이지 위젯 생성
        self.frame = tk.Frame(self.root, width=self.width, height=self.height)

        self.create_nation_listbox()
        self.create_nation_info_textbox()
        self.create_user_message_textbox()

        self.load_image()

        self.home_button = ttk.Button(self.frame, image=self.home_icon, command=self.controller.show_home_page)
        self.email_address_entry = ttk.Entry(self.frame, width=200)
        # 여기서는 이메일을 직접 보내야함
        self.email_button = ttk.Button(self.frame, image=self.email_icon, command=self.controller.show_email_page)

        self.place_widgets()

    def create_nation_listbox(self):
        self.favorite_nation_listbox_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.3),
                                             height=int(float(self.height) * 0.8),
                                             bg='lightblue')

        self.listbox_scrollbar = tk.Scrollbar(self.favorite_nation_listbox_frame)
        self.listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self.favorite_nation_listbox_frame, yscrollcommand=self.listbox_scrollbar.set)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox_scrollbar.config(command=self.listbox.yview)

    def create_nation_info_textbox(self):
        self.favorite_nation_info_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.7),
                                             height=int(float(self.height) * 0.5),
                                             bg='lightblue')

        self.info_scrollbar = tk.Scrollbar(self.favorite_nation_info_frame)
        self.info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text = tk.Text(self.favorite_nation_info_frame, yscrollcommand=self.info_scrollbar.set)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # 나중에 여기서 정보를 기입
        for x in range(100):
            self.info_text.insert(tk.END, "{0}: Line Test\n".format(x))
        self.info_text.config(state='disabled')
        self.info_scrollbar.config(command=self.info_text.yview)

    def create_user_message_textbox(self):
        self.user_message_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.7),
                                                   height=int(float(self.height) * 0.3),
                                                   bg='lightgrey')

        self.user_message_scrollbar = tk.Scrollbar(self.user_message_frame)
        self.user_message_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_text = tk.Text(self.user_message_frame, yscrollcommand=self.user_message_scrollbar.set)
        self.message_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.user_message_scrollbar.config(command=self.message_text.yview)

    def load_image(self):
        home_icon = Image.open("Resource/Home_icon.png")
        home_icon = home_icon.resize((60, 60))
        self.home_icon = ImageTk.PhotoImage(home_icon)

        # search_icon = Image.open("Resource/Search_icon.png")
        # search_icon = search_icon.resize((60, 60))
        # self.search_icon = ImageTk.PhotoImage(search_icon)

        # star_icon = Image.open("Resource/Star_icon.png")
        # star_icon = star_icon.resize((60, 60))
        # self.star_icon = ImageTk.PhotoImage(star_icon)

        email_icon = Image.open("Resource/Gmail_icon.png")
        email_icon = email_icon.resize((60, 60))
        self.email_icon = ImageTk.PhotoImage(email_icon)

    def place_widgets(self):
        # 두 번째 페이지 위젯 배치
        self.favorite_nation_listbox_frame.place(x=0, y=0, width=int(float(self.width) * 0.3),
                                        height=int(float(self.height) * 0.8))

        self.favorite_nation_info_frame.place(x=int(float(self.width) * 0.3), y=0,
                                              width=int(float(self.width) * 0.7), height=int(float(self.height) * 0.5))
        self.user_message_frame.place(x=int(float(self.width) * 0.3), y=int(float(self.height) * 0.5),
                                              width=int(float(self.width) * 0.7), height=int(float(self.height) * 0.3))

        self.home_button.place(x=0, y=425, width=75, height=75)
        self.email_address_entry.place(x=125, y=475, width=200)
        self.email_button.place(x=325, y=425, width=75, height=75)

    def show(self):
        self.frame.place(x=0, y=0, width=self.width, height=self.height)
        # 나중에 읽어온 국가명을 여기에 넣음
        self.listbox.delete(0, tk.END)
        for index, country in enumerate(self.controller.complete_country_list):
            if country['country_id'] in self.controller.favorite_list:
                self.listbox.insert(tk.END, f"{country['country_name']}")

    def hide(self):
        self.frame.place_forget()