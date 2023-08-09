# блок импортов
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler
from config import TOKEN
import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext.filters import Filters
from constans import *
from stikers import *

def start(update: Update, context: CallbackContext):
    keyboard = [[GO]]
    marcup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_sticker(random.choice(HELLO_STIK))
    update.message.reply_text(
        f"есть  загаданное слово если вы угадали букву,но она не в том месте это корова,если вы угадали букву и она в том месте это бык (в любое вряме вы можете написать /cancel и закончить игру)",
        reply_markup=marcup)
    return LEVEL


def begin(update: Update, context: CallbackContext):
    difficulty = update.message.text
    count = LEVELS[difficulty]
    money = context.user_data["coins"]
    difficulty = update.message.text
    if money < MEDIUM_PRICE and difficulty == MEDIUM:
        difficulty = EASY
        update.message.reply_text(
            "У вас недостаточно средств,к сожалению или к счастью мы вас переносим на уровень 'easy'")
    elif money < HARD_PRICE and difficulty == HARD:
        difficulty = EASY
        update.message.reply_text(
            "У вас недостаточно средств,к сожалению или к счастью мы вас переносим на уровень 'easy'")
    elif difficulty == MEDIUM:
        money -= MEDIUM_PRICE
        update.message.reply_text(f"вы преобрели медиум")
    elif difficulty == HARD:
        money -= HARD_PRICE
        update.message.reply_text(f"вы преобрели хард")

    context.user_data["difficulty"] = count

    with open(f"cows_and_buls2/{difficulty}_{count}.txt", encoding="utf-8") as file:
        words = file.read().split("\n")
    secret_word = random.choice(words).strip()
    context.user_data["секрет"] = secret_word  # записыва
    update.message.reply_text(
        f"введите слово из {count} букв")
    return GAME


def chose_level(update: Update, context: CallbackContext):
    with open(f"cows_and_buls2/coins.txt", encoding="utf-8") as file:
        coins = file.read()
    context.user_data["coins"] = int(coins)
    context.user_data["attemps"] = 0
    update.message.reply_text(
        'у вас {money} монет. слово уровня easy: бесплатно ,medium: 5 монет hard:15 монет,на изи уровне дают две монеты,на медиуме 4,а на харде 6')
    keyboard = [[EASY], [MEDIUM], [HARD]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True,
                                 input_field_placeholder="Выбери что тебе по силам")
    update.message.reply_text("Выбери уровень сложности",
                              reply_markup=markup)
    return BEGIN


def game(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    my_word = update.message.text
    secret_word = context.user_data["секрет"]  # достаю
    if len(secret_word) != len(my_word):
        update.message.reply_text(
            f"Количество букв должно быть {len (my_word)}.")
        return None
    bulls = 0
    cows = 0
    for index, letter in enumerate(my_word):
        if letter in secret_word:
            if secret_word[index] == my_word[index]:
                bulls += 1
            else:
                cows += 1
    word_cow = incline_words(COW, cows)
    word_bull = incline_words(BULL, bulls)
    update.message.reply_text(
        f"в вашем слове {bulls} {word_bull} и {cows} {word_cow}", reply_markup=ReplyKeyboardRemove())
    # update.message.reply_text(f"{bulls}  и {len(secret_word)} ")
    if bulls == len(secret_word):
        update.message.reply_text(
            f"вы победили поздравляем", reply_markup=ReplyKeyboardRemove())
        change_money(context, plus=True)
        del context.user_data["секрет"]
        update.message.reply_text(f"слово загаданно")
        return


def end(update: Update, context: CallbackContext):
    if "секрет" in context.user_data:
        secret_word = context.user_data["секрет"]
        update.message.reply_text(f"Загаданное слово было {secret_word}")
        change_money(context, plus=False)
    update.message.reply_text(
        f"доброго дня или вечера", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


# если выклюатель включен, то прибавляет,выключен - отнимаем
def change_money(context, plus=False):
    difficulty = context.user_data["difficulty"]
    money = context.user_data["coins"]
    if plus == False:  # если мы вичитаем
        money *= -1  # делаем число отрицательным
    money += int (difficulty)  # прибавляем или отнимаем монеты


def incline_words(animal: pymorphy2.analyzer.Parse, count: int):
    if count == 1:
        animal = animal.inflect({"nomn"}).word  # бык корова
    elif count in [2, 3, 4]:
        animal = animal.inflect({"gent"}).word  # быка коровы
    else:
        animal = animal.inflect({"gent", "plur"}).word  # быков коров
    return animal


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
