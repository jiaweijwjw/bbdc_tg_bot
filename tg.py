from creds import API_KEY, CHAT_ID
import requests


class TelegramChatbot:
    def __init__(self):
        self.api_key = API_KEY
        self.chat_id = CHAT_ID
        self.base_url = "https://api.telegram.org/bot{}/".format(self.api_key)

    def send_practical_training_slots(self, msg):
        url = self.base_url + "sendMessage?chat_id={}&text={}".format(self.chat_id, msg)
        if msg is not None:
            requests.get(url)
