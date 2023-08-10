#блок импортов
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler
from telegram.ext.filters import Filters
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from cows_and_buls2.config import TOKEN


GENDER, NAME, SURNAME, NUMBER, RESULT = range(5)
MALE, FEMALE, OTHER = "мужской","женский","другой"
NEXT = "дальше"
#блок функций
def start(update: Update, context: CallbackContext):
    # update - входяшее сообщениеб context это чат в целом
    keyboard = [[MALE, FEMALE, OTHER]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="выберите пол")
    bot_name = context.bot.name
    update.message.reply_text(f"я бот меня зовут {bot_name}", reply_markup= markup)
    update.message.reply_text(f"Начинаю сбор информации. выберите пол")
    return GENDER#ПЕРЕХОД К СЛЕДУЮЩЕМУ ШАГУ

def end(update: Update, context: CallbackContext):
    update.message.reply_text(f"значит ты выбрал конец")
    return ConversationHandler.END
    
def get_gender(update: Update, context: CallbackContext):
    gender = update.message.text
    context.user_data["gender"] = gender
    update.message.reply_text(f"введите имя",reply_markup=ReplyKeyboardRemove())
    return NAME
    
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
    keyboard = [[NEXT]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="нажмите дальше")
    context.user_data["number"] = number
    update.message.reply_text(f"Сбор информации завершен", reply_markup= markup)
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

#хендлеры
contact_handler = ConversationHandler(
    entry_points=[CommandHandler("start",start)],
    states={
            GENDER:[MessageHandler(Filters.regex(f"^({MALE}|{FEMALE}|{OTHER})$"),get_gender)],
            NAME:[MessageHandler(Filters.text & ~Filters.command, get_name)],
            SURNAME:[MessageHandler(Filters.text & ~Filters.command, get_surname)],
            NUMBER:[MessageHandler(Filters.text & ~Filters.command, get_number)],
            RESULT:[MessageHandler(Filters.regex(f"^({NEXT})$"), get_result)]
        },
    fallbacks=[CommandHandler("end",end)]
)
#добавляем хендлеры диспечеру
dispatcher.add_handler(contact_handler)

print("server started")
updater.start_polling()--
updater.idle()

# git clone https://github.com/SavStep/andromeda-learning.git .
# git pull