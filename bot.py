import os
import telebot
import time
import random
from telebot import types

TOKEN = os.environ.get("6594665064:AAFKNuMQwgO2WgYgDvpF0RgjF4Teo1DMfuA")
bot = telebot.TeleBot(TOKEN)

authorized_user_ids = ["@DirtyBand"]

def generate_random_token():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=10))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! يمكنك استخدام أمر /generate لإنشاء رمز مؤقت.")

@bot.message_handler(func=lambda message: message.text == "توليد رمز")
def generate_token(message):
    user_id = message.from_user.id
    if str(user_id) in authorized_user_ids:
        global temp_token, token_expiration
        temp_token = generate_random_token()
        
        markup = types.ReplyKeyboardMarkup(row_width=2)
        item1 = types.KeyboardButton("24 ساعة")
        item2 = types.KeyboardButton("96 ساعة")
        item3 = types.KeyboardButton("30 يوم")
        markup.add(item1, item2, item3)
        
        bot.send_message(message.chat.id, f"تم إنشاء رمز مؤقت: {temp_token}\nيرجى اختيار مدة الصلاحية:", reply_markup=markup)
        bot.register_next_step_handler(message, set_token_expiration)
    else:
        bot.send_message(message.chat.id, "ليس لديك الحق في استخدام هذا البوت.")

def set_token_expiration(message):
    global token_expiration
    if message.text == "24 ساعة":
        token_expiration = time.time() + (24 * 60 * 60)
    elif message.text == "96 ساعة":
        token_expiration = time.time() + (96 * 60 * 60)
    elif message.text == "30 يوم":
        token_expiration = time.time() + (30 * 24 * 60 * 60)
    bot.send_message(message.chat.id, "تم تعيين مدة صلاحية الرمز بنجاح.")

@bot.message_handler(func=lambda message: message.text == "استخدام البوت")
def use_bot(message):
    user_id = message.from_user.id
    current_time = time.time()
    if str(user_id) in authorized_user_ids and current_time <= token_expiration:
        bot.send_message(message.chat.id, "بإمكانك البدء في استخدام البوت الآن.")
    else:
        bot.send_message(message.chat.id, "ليس لديك الحق في استخدام البوت في الوقت الحالي.")

bot.polling()
