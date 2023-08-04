#блок импортов
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler
from telegram.ext.filters import Filters
from telegram import Update
from config import TOKEN

NAME, SURNAME, NUMBER, RESULT = range(4)

#блок функций
def start(update: Update, context: CallbackContext):
    # update - входяшее сообщениеб context это чат в целом
    bot_name = context.bot.name
    update.message.reply_text(f"я бот меня зовут {bot_name}")
    update.message.reply_text(f"Начинаю сбор информации. Назовите свое имя")
    return NAME#ПЕРЕХОД К СЛЕДУЮЩЕМУ ШАГУ

def end(update: Update, context: CallbackContext):
    update.message.reply_text(f"значит ты выбрал конец")
    
def get_name(update: Update, context: CallbackContext):
    name = update.message.text
    context.user_data["name"] = name
    update.message.reply_text(f"Теперь введите фамилию")
    return SURNAME

def get_surname(update: Update, context: CallbackContext):
    surname = update.message.text
    context.user_data["surname"] = surname
    update.message.reply_text(f"Введите номер телефона")
    return NUMBER

def get_number(update: Update, context: CallbackContext):
    number = update.message.text
    if not number.isdigit():
        update.message.reply_text("Введите номер телефона в формате 8xxxxxxxxxx")
        return None
    context.user_data["number"] = number
    update.message.reply_text(f"Сбор информации завершен. Отправьте любой текст, чтобы увидеть результат")
    return RESULT

def get_result(update: Update, context: CallbackContext):
    name = context.user_data["name"]
    surname = context.user_data["surname"]
    number = context.user_data["number"]
    update.message.reply_contact(number, f"{name}", surname)
    return ConversationHandler.END
    
#сам бот и его зам
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

#обработчики



#хендлеры
contact_handler = ConversationHandler(
    entry_points=[CommandHandler("start",start)],
    states={
            NAME:[MessageHandler(Filters.text, get_name)],
            SURNAME:[MessageHandler(Filters.text, get_surname)],
            NUMBER:[MessageHandler(Filters.text, get_number)]
        },
    fallbacks=[CommandHandler("end",end)]
)
#добавляем хендлеры диспечеру
dispatcher.add_handler(contact_handler)

print("server started")
updater.start_polling()
updater.idle()

