#блок импортов
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler
from telegram.ext.filters import Filters
from config import TOKEN
from functions import *
#сам бот и его зам
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

#хендлеры
contact_handler = ConversationHandler(
    entry_points=[CommandHandler("start",start)],
    states={ 
         GAME: [MessageHandler(Filters.text & ~Filters.command, game)]
        },
    fallbacks=[CommandHandler("end",end)]
)
#добавляем хендлеры диспечеру
dispatcher.add_handler(contact_handler)

print("server started")
updater.start_polling()
updater.idle()
