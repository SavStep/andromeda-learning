# блок импортов
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler
from config import TOKEN
import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext.filters import Filters
from constans import *


def start(update: Update, context: CallbackContext):
    keyboard = [[GO]]
    marcup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        f"есть загаданное слово (у нас из 3 букв)если вы угадали букву,но она не в том месте это корова,если вы угадали букву и она в том месте это бык (в любое вряме вы можете написать /cancel и закончить игру)",
        reply_markup=marcup)
    return LEVEL

def chose_level(update: Update, context: CallbackContext):
    keyboard = [[EASY], [MEDIUM], [HARD]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True,
                                 input_field_placeholder="Выбери что тебе по силам")
    update.message.reply_text("Выбери уровень сложности",
                              reply_markup=markup)
    return BEGIN

def begin(update: Update, context: CallbackContext):
    difficulty = update.message.text
    count = LEVELS[difficulty]
    with open(f"cows_and_buls2/{difficulty}_{count}.txt", encoding="utf-8") as file:
        words = file.read().split("\n")
    secret_word = random.choice(words)
    context.user_data["секрет"] = secret_word  # записыва
    update.message.reply_text(
        f"Есть загаданное слово (у нас из {count} букв)если вы угадали букву,но она не в том месте это корова,если вы угадали букву и она в том месте это бык")
    return GAME





def game(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    my_word = update.message.text
    secret_word = context.user_data["секрет"]  # достаю
    if len(secret_word) != len(my_word):
        update.message.reply_text(f"буквы не совпадают")
        return None
    bulls = 0
    cows = 0
    for index, letter in enumerate(my_word):
        if letter in secret_word:
            if secret_word[index] == my_word[index]:
                bulls += 1
            else:
                cows += 1
    update.message.reply_text(f"в вашем слове {bulls} быков и {cows} коров", reply_markup=ReplyKeyboardRemove())
    # update.message.reply_text(f"{bulls}  и {len(secret_word)} ")
    if bulls == len(secret_word):
        update.message.reply_text(f"вы победили поздравляем")
        del context.user_data["секрет"]
        update.message.reply_text(f"слово загаданно")
        return


def end(update: Update, context: CallbackContext):
    update.message.reply_text(f"доброго дня или вечера")
    return ConversationHandler.END


# блок хендлеров
game_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        LEVEL: [MessageHandler(Filters.regex(f"^({GO})$"), chose_level)],
        BEGIN: [MessageHandler(Filters.regex(f"^({EASY}|{MEDIUM}|{HARD})$"), begin)],
        GAME: [MessageHandler(Filters.text & ~Filters.command, game)],

    },
    fallbacks=[CommandHandler("cancel", end), CommandHandler("stop", end)]


)


# сам бот и его зам
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

# работники диспечера
dispatcher.add_handler(game_handler)


print("бот запущен")
updater.start_polling()
updater.idle()
