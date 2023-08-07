#блок импортов
from contact_bot.turnip.config import TOKEN
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
from pathlib import Path


#блок функций
def start(update: Update, context: CallbackContext):
    # update - входяшее сообщениеб context это чат в целом
    bot_name = context.bot.name
    update.message.reply_text(f"я бот меня зовут {bot_name}")
    update.message.reply_text(f"""
                              Вот что могу:
                              /hello - я могу с тобой поздароваться ;)
                              /bye - и я могу с тобой попращаться:0
                              /contact - контакт автора :]
                              /animation - я могу скинуть гифку ^_^
                              /audio - также я могу скинуть звук морского
                              льва*_* 
                              """)
    update.message.reply_photo("https://kartinkof.club/uploads/posts/2022-03/1648370947_4-kartinkof-club-p-nu-privet-mem-4.jpg")
    
def hello(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name      
    update.message.reply_text(f"Доброго дня сударь, {user_name}")
    
def bye(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name      
    context.bot.send_message(update.effective_chat.id, f"хорошего дня или вечера сударь(ыня), {user_name}")
    
def send_contact(update: Update, context: CallbackContext):
    update.message.reply_contact(f"8 (917) 296 09 64", "автор", "кода")
   
def echo(update: Update, context: CallbackContext):
    message = context.args # получаем сообщение после /echo
    if not message:# если сообщение пустое
        update.message.reply_text("после команды .echo нужно набрать сообщение через пробел")
        return None#
    message= " ".join(message)# объединяем сообщение
    update.message.reply_text(message) # отправляем сообщение
    print (message)
def animation(update: Update, context: CallbackContext):
    update.message.reply_animation(f"https://hips.hearstapps.com/pop.h-cdn.co/assets/17/24/640x320/landscape-1497533116-not-dead.gif?resize=640:*")
def send_audio(update: Update, context: CallbackContext):
    update.message.reply_audio( Path(f"first_bot/audio/mp3_466228.mp3").read_bytes())
    
#блок хендлеров
start_handler =CommandHandler("start", start)
hello_handler =CommandHandler("hello", hello)
bye_handler =CommandHandler("bye", bye)
contact_handler =CommandHandler("contact", send_contact)
echo_handler =CommandHandler("echo", echo)
animation_handler =CommandHandler("animation", animation)
audio_handler =CommandHandler("audio", send_audio)

#бот
updater = Updater(TOKEN) #ядро нашего бота 
dispatcher = updater.dispatcher


#работники диспечера
dispatcher.add_handler(start_handler)
dispatcher.add_handler(hello_handler)
dispatcher.add_handler(bye_handler)
dispatcher.add_handler(contact_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(animation_handler)
dispatcher.add_handler(audio_handler)

print("бот запущен")
updater.start_polling() #запускает обновления
updater.idle()

