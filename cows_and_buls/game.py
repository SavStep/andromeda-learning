# блок импортов
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler
from config import TOKEN
import random
from telegram import Update
from telegram.ext.filters import Filters
#
    
def getaway(update: Update, context: CallbackContext):
    user_name = update._effective_user.first_name
    message = update.message.text    
    with open("cows_and_buls\words.txt", encoding="utf-8") as file:
        words = file.read().split("/n")
    secret_word = random.choice(secret_word) 
    context.user_data["секрет"] = secret_word
    update.message.reply_text("")
    
    
    

    
    
    
    
#блок обработчиков
message_handler = MessageHandler(Filters.text, getaway)



#сам бот и его зам
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

#работники диспечера
dispatcher.add_handler(message_handler)



print("бот запущен")
updater.start_polling()
updater.idle
