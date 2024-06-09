import time
import telepot
from pprint import pprint
import threading

class TelegramBot:
    def __init__(self, controller, token, service_key):
        self.token = token
        self.service_key = service_key
        self.bot = telepot.Bot(token)
        self.controller = controller
        self.running = False
        self.thread = None

    def reply_country_data(self, country_name, user):
        exist = False
        for index, country in enumerate(self.controller.complete_country_list):
            if country['country_name'] == country_name:
                self.bot.sendMessage(user, country['country_basic'])
                exist = True
                break

        if not exist:
            self.bot.sendMessage(user, f'{country_name}에 대한 정보를 찾을 수 없습니다.')

    def reply_country_population(self, country_name, user):
        exist = False
        for index, country in enumerate(self.controller.complete_country_list):
            if country['country_name'] == country_name:
                self.bot.sendMessage(user, "{0} 인구 수: {1}명".format(country_name, country['population']))
                exist = True
                break

        if not exist:
            self.bot.sendMessage(user, f'{country_name}에 대한 정보를 찾을 수 없습니다.')

    def reply_country_area(self, country_name, user):
        exist = False
        for index, country in enumerate(self.controller.complete_country_list):
            if country['country_name'] == country_name:
                self.bot.sendMessage(user, "{0} 면적: {1}km^2".format(country_name, country['area']))
                exist = True
                break

        if not exist:
            self.bot.sendMessage(user, f'{country_name}에 대한 정보를 찾을 수 없습니다.')

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            self.bot.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
            return

        text = msg['text']
        args = text.split(' ')

        if text.startswith('도움') or text.startswith('help'):
            self.bot.sendMessage(chat_id, '명령어 - 국가 [국가명], 인구 [국가명], 면적 [국가명]')
        elif text.startswith('국가') and len(args) > 1:
            country_name = ' '.join(args[1:])  # '국가' 다음의 모든 단어를 국가 이름으로 취급
            self.reply_country_data(country_name, chat_id)
        elif text.startswith('인구') and len(args) > 1:
            country_name = ' '.join(args[1:])
            self.reply_country_population(country_name, chat_id)
        elif text.startswith('면적') and len(args) > 1:
            country_name = ' '.join(args[1:])
            self.reply_country_area(country_name, chat_id)
        else:
            self.bot.sendMessage(chat_id, '모르는 명령어입니다.\n도움(또는 help), 국가 [국가명], 인구 [국가명], 면적 [국가명]'
                                          ' 형식을 입력하세요.')

    def run(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._message_loop)
        self.thread.start()

    def _message_loop(self):
        pprint(self.bot.getMe())
        self.bot.message_loop(self.handle)
        print('Listening...')
        while self.running:
            time.sleep(10)

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()