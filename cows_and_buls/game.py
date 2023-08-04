# блок импортов
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler
from contact_bot.config import TOKEN
import random
from telegram import Update
from telegram.ext.filters import Filters
#
    
def getaway(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    my_word = update.message.text    
    if "секрет" not in context.user_data:
        with open("cows_and_buls\words.txt", encoding="utf-8") as file:
            words = file.read().split("\n")
        secret_word = random.choice(words) 
        
        context.user_data["секрет"] = secret_word#записываю
    else:
        secret_word = context.user_data["секрет"]#достаю
    if len(secret_word) != len(my_word):
            update.message.reply_text(f"буквы не совпадают")
            return None
    bulls = 0
    cows = 0    
    for index, letter in enumerate(my_word):
        if letter in secret_word:
            if secret_word[index] == my_word[index]:
                bulls+=1
            else:
                cows+=1
    update.message.reply_text(f"в вашем слове {bulls} быков и {cows} коров")
    # update.message.reply_text(f"{bulls}  и {len(secret_word)} ")
    if bulls == len(secret_word):
        update.message.reply_text(f"вы победили поздравляем")
        del context.user_data["секрет"]
    
#блок обработчиков
message_handler = MessageHandler(Filters.text, getaway)



#сам бот и его зам
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

#работники диспечера
dispatcher.add_handler(message_handler)



print("бот запущен")
updater.start_polling()
updater.idle()
