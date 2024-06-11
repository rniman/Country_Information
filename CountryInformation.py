from Home import *
from Search import *
from Favorite import *
from Email import *
from TelegramBot import *

import CountryInfoFetcher as Ci
import os
from googlemaps import Client
import subprocess

service_key = spam.ret_service_key()
token = spam.ret_token()
user = spam.ret_user_id()

FRAME_WIDTH = 400
FRAME_HEIGHT = 500

class CountryInfoGUI:
    def __init__(self, root):
        self.telegram_program = None

        self.root = root
        self.root.title("Country Info")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.width = FRAME_WIDTH
        self.height = FRAME_HEIGHT

        # Google Maps API 클라이언트 생성
        self.Google_API_Key = spam.ret_google_api_key()
        self.gmaps = Client(key=self.Google_API_Key)

        # XML, JSON 읽어오기
        self.fetcher = Ci.CountryInfoFetcher(service_key)
        basic_xml_data = self.fetcher.fetch_country_data(self.fetcher.basic_query)
        overview_json_data = self.fetcher.fetch_country_data(self.fetcher.overview_query)
        accident_xml_data = self.fetcher.fetch_country_data(self.fetcher.accident_query)
        warning_xml_data = self.fetcher.fetch_country_data(self.fetcher.warning_query)

        self.complete_country_list = None
        if basic_xml_data and overview_json_data:
            basic_country_list = self.fetcher.parse_basic_data(basic_xml_data)
            overview_data_list = self.fetcher.parse_overview_data(overview_json_data)
            accident_data_list = self.fetcher.parse_accident_data(accident_xml_data)
            warning_data_list = self.fetcher.parse_warning_data(warning_xml_data)

            self.complete_country_list = self.fetcher.merge_supplement_data(basic_country_list, overview_data_list)
            self.complete_country_list = self.fetcher.merge_accident_data(self.complete_country_list, accident_data_list)
            self.complete_country_list = self.fetcher.merge_warning_data(self.complete_country_list, warning_data_list)

        self.home_page = HomePage(self.root, self)
        self.search_page = SearchPage(self.root, self)
        self.favorite_page = FavoritePage(self.root, self)
        self.email_page = EmailPage(self.root, self)
        self.telegram = TelegramBot(self, token, service_key)

        self.favorite_list = []
        # 관심 국가 리스트 (기본 관심 국가 설정)
        for index, country in enumerate(self.complete_country_list):
            if country['country_name'] in ['영국', '일본', '미국', '베트남', '프랑스']:
                self.favorite_list.append(country['country_id'])
                self.home_page.listbox.itemconfig(index, {'fg': 'lightblue'})
            # gu_center = self.gmaps.geocode(country['country_name'])[0]['geometry']['location']
            # print("{0} {1}: ({2}, {3})".format(index, country['country_name'], gu_center['lat'], gu_center['lng']))
        self.home_page.show()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # 윈도우 닫기 이벤트에 핸들러 연결

    def on_closing(self):
        self.stop_telegram()
        self.root.destroy()  # tkinter 애플리케이션 종료

    def show_home_page(self):
        self.search_page.hide()
        self.favorite_page.hide()
        self.email_page.hide()
        self.home_page.show()

    def show_search_page(self):
        if not self.home_page.selected_country:
            return
        selected_country_index = self.home_page.selection_index
        self.search_page.selected_country_index = selected_country_index
        self.home_page.hide()
        self.email_page.hide()
        self.search_page.show()

    def show_favorite_page(self):
        if not self.home_page.selected_country:
            self.search_page.hide()
            self.home_page.hide()
            self.email_page.hide()
            self.favorite_page.show()
            return
        selected_country_id = self.home_page.selected_country['country_id']
        # selected_country_index = self.home_page.selection_index
        if selected_country_id in self.favorite_list:  # 관심 국가 해제
            self.favorite_list.remove(selected_country_id)
        else:
            self.favorite_list.append(selected_country_id)
            # self.favorite_page.selected_country_id = selected_country_id
            self.search_page.hide()
            self.home_page.hide()
            self.email_page.hide()
            self.favorite_page.show()

        if self.home_page.filter_country:
            for index, country in enumerate(self.home_page.filter_country):
                if country['country_id'] in self.favorite_list:
                    self.home_page.listbox.itemconfig(index, {'fg': 'lightblue'})
                else:
                    self.home_page.listbox.itemconfig(index, {'fg': 'black'})
        else:
            for index, country in enumerate(self.complete_country_list):
                if country['country_id'] in self.favorite_list:
                    self.home_page.listbox.itemconfig(index, {'fg': 'lightblue'})
                else:
                    self.home_page.listbox.itemconfig(index, {'fg': 'black'})

    def release_favorite_page(self):
        selected_country_id = self.home_page.selected_country['country_id']
        if selected_country_id in self.favorite_list:  # 관심 국가 해제
            self.favorite_list.remove(selected_country_id)

        for index, country in enumerate(self.complete_country_list):
            if country['country_id'] in self.favorite_list:
                self.home_page.listbox.itemconfig(index, {'fg': 'lightblue'})
            else:
                self.home_page.listbox.itemconfig(index, {'fg': 'black'})

    def show_email_page(self):
        self.search_page.hide()
        self.home_page.hide()
        self.favorite_page.hide()
        self.email_page.show()

    def show_telegram(self):
        telegram_path = os.path.join(os.getenv('APPDATA'), 'Telegram Desktop', 'Telegram.exe')
        self.telegram_program = subprocess.Popen([telegram_path])
        self.telegram.bot.sendMessage(user, 'Telegram Open')

        # Telegram 봇 실행을 별도의 스레드에서 실행
        self.telegram.run()

    def stop_telegram(self):
        if self.telegram:
            self.telegram.stop()
        if self.telegram_program:
            self.telegram_program.terminate()
            self.telegram_program = None

if __name__ == "__main__":
    root = tk.Tk()
    app = CountryInfoGUI(root)
    root.mainloop()