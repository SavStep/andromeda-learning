# блок импортов
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler
from telegram.ext.filters import Filters
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import TOKEN
import pymorphy2

BEGIN, GAME = range(2)
morph = pymorphy2.MorphAnalyzer()
GO = "вперёд"

# блок функций


def start(update: Update, context: CallbackContext):
    keyboard = [[GO]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(f"Хорошо. Давай поиграем. Ты любишь придумывать сказки? Я – очень люблю. Ты знаешь сказку, как посадил дед репку? А кто помогал её тянуть? Давай придумаем вместе.",
                              reply_markup=markup)
    heroes = [["дедку"], ["дедка", "репку"]]
    context.user_data["heroes"] = heroes
    return BEGIN


def begin(update: Update, context: CallbackContext):
    update.message.reply_text(f" Посадил дед репку. Выросла репка большая-пребольшая. Стал дед репку из земли тянуть. Тянет-потянет, вытянуть не может. Кого позвал дедка?",
                              reply_markup=ReplyKeyboardRemove())
    return GAME
    
def game(update: Update, context: CallbackContext):
    word = update.message.text
    tag = morph.parse(word)[0]
    nomn = tag.inflect({'nomn'}).word
    accs = tag.inflect({'accs'}).word
    heroes = context.user_data["heroes"]
    heroes[0].insert(0, nomn)
    heroes.insert(0, [accs])
    result = ""
    for nom, ac in heroes[1:]:
        result += f"{nom} - за {ac}. ".title()
    update.message.reply_text(result)
    
    
def end(update: Update, context: CallbackContext):
    update.message.reply_text(f"значит ты выбрал конец")
    return ConversationHandler.END


# сам бот и его зам
updater = Updater(TOKEN)
dispatcher = updater.dispatcher


# хендлеры
game_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        BEGIN:[MessageHandler(Filters.regex(f'^({GO})$'), begin)],
        GAME:[MessageHandler(Filters.text & ~Filters.command, game)],
    },
    fallbacks=[CommandHandler("end", end)]
)


# добавляем хендлеры диспечеру
dispatcher.add_handler(game_handler)

print("server started")
updater.start_polling()
updater.idle()
