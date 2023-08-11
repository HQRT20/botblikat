import os
import time
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = "12230620"
API_HASH = "6a754763979dd2cf139687be3e89901d"
BOT_TOKEN = "5765546953:AAG_UdX2moG7ryDHuERp6cXf4yiGGdu58kg"
AUTHORIZED_USER_ID = @DirtyBand

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

authorized_user_ids = [AUTHORIZED_USER_ID]
user_tokens = {}
user_codes = {}

def generate_random_token():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=8))

@app.on_message(filters.private & filters.user(AUTHORIZED_USER_ID))
def start(client, message):
    user_id = message.from_user.id
    user_username = message.from_user.username
    if user_id in authorized_user_ids:
        message.reply_text(f"مرحباً المطور {user_username}!\n\n"
                           "اختر إحدى الخيارات:",
                           reply_markup=InlineKeyboardMarkup(
                               [
                                   [InlineKeyboardButton("بدء رفع البلاغات", callback_data="report"),
                                    InlineKeyboardButton("توليد كود للمستخدم", callback_data="generate_code")]
                               ]
                           ))
    else:
        message.reply_text("ليس لديك الحق في استخدام هذا البوت.")

@app.on_callback_query(filters.user(AUTHORIZED_USER_ID) & filters.regex("report|generate_code"))
def callback_query(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data
    if user_id in authorized_user_ids:
        if data == "report":
            global temp_token
            temp_token = generate_random_token()
            keyboard = [
                [InlineKeyboardButton("1 يوم", callback_data="1d"),
                 InlineKeyboardButton("7 أيام", callback_data="7d"),
                 InlineKeyboardButton("30 يوم", callback_data="30d")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            callback_query.message.edit_text(f"تم إنشاء رمز مؤقت: {temp_token}\nيرجى اختيار مدة الصلاحية:", reply_markup=reply_markup)
        elif data == "generate_code":
            user_code = generate_random_token()
            user_codes[user_id] = user_code
            callback_query.message.edit_text(f"تم توليد كود للمستخدم:\n\n{user_code}\n\n"
                                             "يرجى ارسال هذا الكود للمستخدم لتفعيل استخدام البوت.")
    else:
        callback_query.message.edit_text("ليس لديك الحق في استخدام البوت في الوقت الحالي.")

@app.on_message(filters.private & ~filters.user(AUTHORIZED_USER_ID))
def start(client, message):
    user_id = message.from_user.id
    user_code = message.text
    if user_id in user_codes and user_code == user_codes[user_id]:
        user_tokens[user_id] = time.time() + (24 * 60 * 60)  # قم بتغيير المدة حسب متطلباتك
        message.reply_text("تم تفعيل استخدام البوت. يمكنك البدء في رفع البلاغات.")
    else:
        message.reply_text("ليس لديك الحق في استخدام البوت في الوقت الحالي. يرجى التحقق من الكود والمحاولة مرة أخرى.")

@app.on_message(filters.private & ~filters.user(AUTHORIZED_USER_ID))
def process_user_message(client, message):
    user_id = message.from_user.id
    if user_id in user_tokens and time.time() <= user_tokens[user_id]:
        user_token = user_tokens[user_id]
        selected_emails = ["stopCA@telegram.org", "abuse@telegram.org"]
        email_message = f"بريد المستخدم: {message.text}\nموضوع البلاغ: {message.text}\nالرسالة: {message.text}"
        
        
        
        time.sleep(5)
        inline_keyboard = [
            [InlineKeyboardButton("عدد البلاغات", callback_data="get_report_count")]
        ]
        reply_markup =InlineKeyboardMarkup(inline_keyboard)
        message.reply_text("تم رفع البلاغ. انقر على 'عدد البلاغات' لمعرفة عدد البلاغات التي تم رفعها.", reply_markup=reply_markup)
    else:
        message.reply_text("ليس لديك الحق في استخدام البوت في الوقت الحالي.")

@app.on_callback_query()
def get_report_count(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in user_tokens and time.time() <= user_tokens[user_id]:
        user_token = user_tokens[user_id]
        report_count = 5  # قم بتغييره إلى القيمة الفعلية
        remaining_time = user_tokens[user_id] - time.time()
        callback_query.message.edit_text("عدد البلاغات المرفوعة: {}\nمدة الصلاحية المتبقية: {} ثواني".format(report_count, int(remaining_time)))
    else:
        callback_query.message.edit_text("ليس لديك الحق في استخدام البوت في الوقت الحالي.")

app.run() 
