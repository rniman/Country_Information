from Home import *
from Search import *
from Favorite import *
from Email import *

FRAME_WIDTH = 400
FRAME_HEIGHT = 500

class CountryInfoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Country Info")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.width = FRAME_WIDTH
        self.height = FRAME_HEIGHT

        self.home_page = HomePage(self.root, self)
        self.search_page = SearchPage(self.root, self)
        self.favorite_page = FavoritePage(self.root, self)
        self.email_page = EmailPage(self.root, self)

        # 관심국가 리스트
        self.favorite_list = []
        self.home_page.show()

    def show_home_page(self):
        self.search_page.hide()
        self.favorite_page.hide()
        self.email_page.hide()
        self.home_page.show()

    def show_search_page(self):
        selected_country = self.home_page.listbox.get(tk.ACTIVE)
        self.search_page.detail_info_label.config(text=f"{selected_country} 정보 표시")
        self.home_page.hide()
        self.email_page.hide()
        self.search_page.show()

    def show_favorite_page(self):
        self.search_page.hide()
        self.home_page.hide()
        self.email_page.hide()
        self.favorite_page.show()

    def show_email_page(self):
        self.search_page.hide()
        self.home_page.hide()
        self.favorite_page.hide()
        self.email_page.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = CountryInfoGUI(root)
    root.mainloop()
