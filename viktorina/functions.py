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
    # списокб внутри которого [вопрос, ответ1 ответ2 ответ3 ответ4]
    quetions_list = read_csw()
    random.shuffle(quetions_list)
    length = QUETIONS_ON_ROUND if len(
        quetions_list) > QUETIONS_ON_ROUND else len(quetions_list)
    quetions_list = quetions_list[:length]
    context.user_data["quetions"] = quetions_list
    context.user_data["index"] = 0
    context.user_data["counter"] = 0
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


def game(update: Update, context: CallbackContext):
    quetions_list = context.user_data["quetions"]
    index = context.user_data["index"]
    if "right_answer" in context.user_data:
        right_answer = context.user_data["right_answer"]
        my_answer = update.message.text
        if right_answer == my_answer:
            context.user_data["counter"] += 1
            update.message.reply_sticker(LEVEL_STIK)
            update.message.reply_text("Молодец!")
        else:
            update.message.reply_sticker(MONEY_STIK)
            update.message.reply_text("Ничего страшного!")
    try:
        answers = quetions_list[index]
        question = answers.pop(0)
        right_answer = answers[1]
        random.shuffle(answers)

        keyboard = [
            answers[2:],
            answers[:2]
        ]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text(question, reply_markup=markup)

        context.user_data["index"] += 1
        context.user_data["right_answer"] = right_answer
    except IndexError:
        counter = context.user_data["counter"]
        counter_quetions = len(quetions_list)
        update.message.reply_text(f"правильных ответов: {counter}/{counter_quetions}",
        reply_markup=ReplyKeyboardRemove())
        if counter <=1:
            update.message.reply_sticker(ANGRY_STIK)
        elif counter <=2:
            update.message.reply_sticker(BC_STIK)
        elif counter <=4:
            update.message.reply_sticker(VICTORY_STIK)
            update.message.reply_text(
                "вопросы закончились :(", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
