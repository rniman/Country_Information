from Home import *
from Search import *
from Favorite import *
from Email import *

import CountryInfoFetcher as Ci

service_key = "TM2mB7BkLj7%2B1mK%2FbNgWbxjMPtdffuyVQbT46zhjwGtnC%2FEA6FQwymPyHVNcFFdJN%2FaQuqSYutGF33dW20COZg%3D%3D"

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

        # XML, JSON 읽어오기
        self.fetcher = Ci.CountryInfoFetcher(service_key)
        basic_xml_data = self.fetcher.fetch_country_data(self.fetcher.basic_query)
        overview_json_data = self.fetcher.fetch_country_data(self.fetcher.overview_query)
        self.complete_country_list = None
        if basic_xml_data and overview_json_data:
            basic_country_list = self.fetcher.parse_basic_data(basic_xml_data)
            overview_data = self.fetcher.parse_overview_data(overview_json_data)
            self.complete_country_list = self.fetcher.merge_data(basic_country_list, overview_data)
            # self.fetcher.print_country_data(self.complete_country_list)

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
