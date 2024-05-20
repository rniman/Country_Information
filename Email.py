import tkinter as tk
from tkinter import ttk

class EmailPage:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.width = controller.width
        self.height = controller.height

        self.create_widgets()

    def create_widgets(self):
        # 두 번째 페이지 위젯 생성
        self.frame = tk.Frame(self.root, width=self.width, height=self.height)
        self.favorite_nation_listbox_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.3),
                                             height=int(float(self.height) * 0.8),
                                             bg='lightblue')
        self.favorite_nation_info_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.7),
                                             height=int(float(self.height) * 0.5),
                                             bg='lightblue')
        self.user_message_frame = tk.Frame(self.frame, width=int(float(self.width) * 0.7),
                                                   height=int(float(self.height) * 0.3),
                                                   bg='lightgrey')

        self.listbox_scrollbar = tk.Scrollbar(self.favorite_nation_listbox_frame)
        self.listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self.favorite_nation_listbox_frame, yscrollcommand=self.listbox_scrollbar.set)
        # 나중에 읽어온 국가명을 여기에 넣음
        for i in range(50):
            self.listbox.insert(tk.END, f"Country {i+1}")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox_scrollbar.config(command=self.listbox.yview)

        self.info_scrollbar = tk.Scrollbar(self.favorite_nation_info_frame)
        self.info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text = tk.Text(self.favorite_nation_info_frame, yscrollcommand=self.info_scrollbar)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for x in range(100):
            self.info_text.insert(tk.END, "{0}: Line Test\n".format(x))
        self.info_text.config(state='disabled')
        self.info_scrollbar.config(command=self.info_text.yview)

        self.home_button = ttk.Button(self.frame, text="Home", command=self.controller.show_home_page)
        # 여기서는 이메일을 직접 보내야함
        self.email_button = ttk.Button(self.frame, text="Email", command=self.controller.show_email_page)

        self.place_widgets()

    def place_widgets(self):
        # 두 번째 페이지 위젯 배치
        self.favorite_nation_listbox_frame.place(x=0, y=0, width=int(float(self.width) * 0.3),
                                        height=int(float(self.height) * 0.8))

        self.favorite_nation_info_frame.place(x=int(float(self.width) * 0.3), y=0,
                                              width=int(float(self.width) * 0.7), height=int(float(self.height) * 0.5))
        self.user_message_frame.place(x=int(float(self.width) * 0.3), y=int(float(self.height) * 0.5),
                                              width=int(float(self.width) * 0.7), height=int(float(self.height) * 0.3))

        self.home_button.place(x=0, y=425, width=75, height=75)
        self.email_button.place(x=325, y=425, width=75, height=75)

    def show(self):
        self.frame.place(x=0, y=0, width=self.width, height=self.height)

    def hide(self):
        self.frame.place_forget()