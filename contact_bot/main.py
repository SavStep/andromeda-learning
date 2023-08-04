#блок импортов
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler
from telegram.ext.filters import Filters
from telegram import Update
from config import TOKEN

NAME = 1

#блок функций
def start(update: Update, context: CallbackContext):
    # update - входяшее сообщениеб context это чат в целом
    bot_name = context.bot.name
    update.message.reply_text(f"я бот меня зовут {bot_name}")
    return NAME#ПЕРЕХОД К СЛЕДУЮЩЕМУ ШАГУ

def end(update: Update, context: CallbackContext):
    update.message.reply_text(f"значит ты выбрал конец")
def get_name(update: Update, context: CallbackContext):
    name = update.message.text
    update.message.reply_text(f"Вы ввели {name}")

#сам бот и его зам
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

#обработчики



#хендлеры
contact_handler = ConversationHandler(
    entry_points=[CommandHandler("start",start)],
    states={
            NAME:{MessageHandler}
        },
    fallbacks=[CommandHandler("end",end)]
)
#добавляем хендлеры диспечеру
dispatcher.add_handler(contact_handler)

print("server started")
updater.start_polling()
updater.idle()

