import os
import telebot
import time
import random
from telebot import types

bot_token = "6594665064:AAFKNuMQwgO2WgYgDvpF0RgjF4Teo1DMfuA"
bot = telebot.TeleBot(bot_token)

authorized_user_ids = ["5805203780"]
active_reports = True

# تعريف الرمز المؤقت والزمن المحدد للاستخدام
temp_token = None
token_expiration = None

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if str(user_id) in authorized_user_ids:
        markup = types.ReplyKeyboardMarkup(row_width=1)
        item = types.KeyboardButton("رفع بلاغ")
        item2 = types.KeyboardButton("توليد رمز")
        markup.add(item, item2)
        bot.send_message(message.chat.id, "مرحبًا بك! اضغط على الخيار المناسب.", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "ليس لديك الحق في استخدام هذا البوت.")

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
    
    bot.send_message(message.chat.id, f"تم تحديد صلاحية الرمز لمدة {message.text}.")
    
# تابع باقي الأكواد الموجودة في السورس السابق...

bot.polling()
