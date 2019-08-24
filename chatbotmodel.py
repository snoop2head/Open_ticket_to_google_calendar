import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters  # import modules

class TelegramBot:
    def __init__(self, name, token):
        self.core = telegram.Bot(token)
        self.updater = Updater(token)
        self.id = "self_id_here_as_integer"
        self.name = name

    def sendMessage(self, text):
        self.core.sendMessage(chat_id = self.id, text=text)

    def stop(self):
        self.updater.start_polling()
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()

class baekcloud_bot(TelegramBot):
    def __init__(self):
        self.token = 'your_token_here'
        TelegramBot.__init__(self, 'baekcloud', self.token)
        self.updater.stop()

    def add_handler(self, cmd, func):
        self.updater.dispatcher.add_handler(CommandHandler(cmd, func))

    def start(self):
        self.sendMessage('Hi there!')
        self.updater.start_polling()
        self.updater.idle()
