from telegram.ext import Updater, CommandHandler, MessageHandler, Filters  # import modules
import chatbotmodel
import telegram
from app import google_calendar_writer

#token settings
baekcloud_token = 'input_your_token_here'
baekcloud = telegram.Bot(token = baekcloud_token)
updates = baekcloud.getUpdates()

# message reply function
# update is json format

def get_message(bot , update) :
    if update.message.text == "bye":
        baekcloud.sendMessage('Bye Bye My Blue')
        baekcloud.stop()
    else:
        update.message.reply_text("I got your artist: " + str(update.message.text) + "!" + " please wait until I write on the calendar")
        google_calendar_writer(update.message.text)
        update.message.reply_text("I have finished writing! check your calendar")


updater = Updater(baekcloud_token)

message_handler = MessageHandler(Filters.text, get_message)
updater.dispatcher.add_handler(message_handler)

baekcloud= chatbotmodel.baekcloud_bot()

updater.start_polling(timeout=3, clean=True)
updater.idle()

baekcloud.start()
