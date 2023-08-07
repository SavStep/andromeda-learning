# блок импортов
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler
from contact_bot.turnip.config import TOKEN
import random
from telegram import Update
from telegram.ext.filters import Filters

def start(update: Update, context: CallbackContext, message:list):
    bot_name = context.bot.name
    update.message.reply_text(f"""
                              я бот калькулятор введи команду,а затем два числа
                              /plus - складывать
                              /minus - вычитать
                              /multiply - умножать
                              /divide - делить
                              """)

def get_factorial(update: Update, context: CallbackContext, message:list):
    num = context.args
    if not num or len(num) != 1 or not num[0].isdigit():
        update.message.reply("Введите одно число")
        return None
    num = int(num.pop())
    factorial = 1
    factorial_list = []
    for i in range (1, num+1):
        factorial *= i
        factorial_list.append(factorial)
    update.message.reply_text(f"{factorial_list}")

def make_eval(update: Update, context: CallbackContext, message:list):#не кал бек функция(вспомогательная)
    
    if not message or len(message) != 2:
        update.message.reply_text("Введите два числа через пробел после команды")
        return None
    num1, num2 = message
    if not num1.isdigit() or not num2.isdigit():
        update.message.reply_text("вводить можно только числа")
        return None
    num1,num2 = int(num1), int(num2)
    return num1, num2

def plus(update: Update, context: CallbackContext): #калбек функция 
    message = context.args #это сообщение после команды
    num1, num2= make_eval(update, context,message)
    result = num1 + num2
    update.message.reply_text(f"это будет {result}")
    
    
    
    
def minus(update: Update, context: CallbackContext):
    message = context.args #это сообщение после команды
    num1, num2= make_eval(update, context,message)
    result = num1 - num2
    update.message.reply_text(f"это будет {result}")
        
def multiply(update: Update, context: CallbackContext):
    message = context.args #это сообщение после команды
    num1, num2= make_eval(update, context,message)
    result = num1 * num2
    update.message.reply_text(f"это будет {result}")
def divide(update: Update, context: CallbackContext):
    message = context.args #это сообщение после команды
    num1, num2= make_eval(update, context,message)
    if num2 == 0:
        update.message.reply_text("на ноль делить нельзя")
        return None
    result = num1 / num2
    update.message.reply_text(f"это будет {result}")
    
def getaway(update: Update, context: CallbackContext):
    user_name = update._effective_user.first_name
    message = update.message.text    
    if message == "привет":
        update.message.reply_text(f"привет, {user_name}")
    elif message == "пока":
        update.message.reply_text(f"пока, {user_name}")
    elif "Савели" in message:
        answers = ["О, это мой создатель", "Савелий - лентяй", "знаю такого"]
        update.message.reply_text(f"{random.choice(answers)}")
    elif "мандари" in message:
        answers = ["оо,кому-то будет вкусно", "с новым годом!", "ай,в глаз попал сок от мандарина"]
        update.message.reply_text(f"{random.choice(answers)}")
    elif "иде" in message:
        answers = ["'у тебя появилась лампочка над головой'"]
        update.message.reply_text(f"{random.choice(answers)}")
    
#блок обработчиков
plus_hadler = CommandHandler("plus", plus)
minus_hadler = CommandHandler("minus", minus)
multiply_hadler = CommandHandler("multiply", multiply)
divide_hadler = CommandHandler("multiply", multiply)
message_handler = MessageHandler(Filters.text, getaway)


#сам бот и его зам
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

#работники диспечера
dispatcher.add_handler(plus_hadler)
dispatcher.add_handler(minus_hadler)
dispatcher.add_handler(multiply_hadler)
# dispatcher.add_handler(divide_hadler)
dispatcher.add_handler(message_handler)



print("бот запущен")
updater.start_polling()
updater.idle
