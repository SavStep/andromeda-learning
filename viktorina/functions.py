from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from constants import *
import csv
from stikers import *
import random

def start(update: Update, context: CallbackContext):
    keyboard = [[GO]]
    marcup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_sticker(random.choice(HELLO_STIK))
    update.message.reply_text(
        f"Добро пожаловать в викторину по фортнайт,отвечай на вопросы,выбирая 1 из 4 вариантов ответа,только отвечай правильно!!!",
        reply_markup=marcup)
    quetions_list = read_csw()# списокб внутри которого [вопрос, ответ1 ответ2 ответ3 ответ4]  
    random.shuffle(quetions_list)
    length = QUETIONS_ON_ROUND if len (quetions_list) > QUETIONS_ON_ROUND else len(quetions_list)
    context.user_data["quetions"] = quetions_list
    context.user_data["index"] = 0
    return GAME

    
def read_csw():
    with open("viktorina/database.csv", encoding="utf-8") as file:
        read_data = list(csv.reader(file, delimiter="|"))
        return read_data



def write_to_csv(row):
    with open("viktorina/database.csv", mode="a", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="|", lineterminator="\n")
        writer.writerow(row)
      
def end(update: Update, context: CallbackContext):
    update.message.reply_sticker(END_STIK)
    update.message.reply_text(
        f"ты выбрал конец,амням грустит", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def game(update:Update, context:CallbackContext):
    quetions_list = context.user_data["quetions"]
    index = context.user_data["index"]
    answers = quetions_list[index]
    question = answers.pop(0)
    update.message.reply_text(question)