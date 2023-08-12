import os
import time
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = "12230620"
API_HASH = "6a754763979dd2cf139687be3e89901d"
BOT_TOKEN = "5765546953:AAG_UdX2moG7ryDHuERp6cXf4yiGGdu58kg"
AUTHORIZED_USER_ID = "@DirtyBand"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

authorized_user_ids = [int(AUTHORIZED_USER_ID)]
user_tokens = {}
user_codes = {}
report_emails = ["stopCA@telegram.org", "abuse@telegram.org"]

def generate_random_token():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=8))

@app.on_message(filters.private & filters.user(AUTHORIZED_USER_ID))
def start(client, message):
    user_id = message.from_user.id
    user_username = message.from_user.username
    if user_id in authorized_user_ids:
        message.reply_text(f"مرحبًا المطور {user_username}!\n\n"
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
            callback_query.message.edit_text("يرجى إرسال عنوان البريد الإلكتروني الذي سيتم رفع البلاغ منه:")
            user_codes[user_id] = temp_token
            user_tokens[user_id] = "report_email"
        elif data == "generate_code":
            keyboard = [
                [InlineKeyboardButton("يوم واحد", callback_data="1d"),
                 InlineKeyboardButton("أسبوع", callback_data="7d"),
                 InlineKeyboardButton("30 يومًا", callback_data="30d")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            callback_query.message.edit_text("يرجى اختيار مدة صلاحية الكود:", reply_markup=reply_markup)
            user_tokens[user_id] = "generate_code"
    else:
        callback_query.message.edit_text("ليس لديك الحق في استخدام البوت في الوقت الحالي.")

@app.on_callback_query(filters.user(AUTHORIZED_USER_ID) & filters.regex("1d|7d|30d"))
def callback_query(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data
    if user_id in authorized_user_ids:
        if user_tokens[user_id] == "generate_code":
            user_code = generate_random_token()
            user_codes[user_id] = user_code
            if data == "1d":
                user_tokens[user_id] = time.time() + (1 * 24 * 60 * 60)
                callback_query.message.edit_text(f"تم توليد كود للمستخدم:\n\n{user_code}\n\n"
                                                 f"تم تفعيله لمدة يوم واحد.")
            elif data == "7d":
                user_tokens[user_id] = time.time() + (7 * 24 * 60 * 60)
                callback_query.message.edit_text(f"تم توليد كود للمستخدم:\n\n{user_code}\n\n"
                                                 f"تم تفعيله لمدة أسبوع.")
            elif data == "30d":
                user_tokens[user_id] = time.time() + (30 * 24 * 60 * 60)
                callback_query.message.edit_text(f"تم توليد كود للمستخدم:\n\n{user_code}\n\n"
                                                 f"تم تفعيله لمدة 30 يومًا.")
    else:
        callback_query.message.edit_text("ليس لديك الحق في استخدام البوت في الوقت الحالي.")
        @app.on_message(filters.private & ~filters.user(AUTHORIZED_USER_ID))
def process_user_message(client, message):
    user_id = message.from_user.id
    user_text = message.text
    if user_id in user_tokens and user_tokens[user_id] == "report_email":
        user_tokens[user_id] = "report_subject"
        user_codes[user_id] = user_text
        message.reply_text("يرجى إرسال عنوان موضوع البلاغ:")
    elif user_id in user_tokens and user_tokens[user_id] == "report_subject":
        user_tokens[user_id] = "report_message"
        user_codes[user_id] = user_text
        message.reply_text("يرجى إرسال نص البلاغ:")
    elif user_id in user_tokens and user_tokens[user_id] == "report_message":
        user_tokens[user_id] = "report_photo"
        user_codes[user_id] = user_text
        keyboard = [[InlineKeyboardButton("نعم", callback_data_report_emails[user_id]["subject"] = message.text
            message.reply_text("يرجى إرسال رسالة البلاغ.")
        elif "message" not in user_report_emails[user_id]:
            user_report_emails[user_id]["message"] = message.text
            message.reply_text("هل ترغب في إرسال صورة مع البلاغ؟ (نعم/لا)")
        elif "photo" not in user_report_emails[user_id]:
            if message.text.lower() == "نعم":
                user_report_emails[user_id]["photo"] = True
                message.reply_text("يرجى إرسال الصورة الآن.")
            elif message.text.lower() == "لا":
                user_report_emails[user_id]["photo"] = False
                send_report_thread(user_id,
                                   user_report_emails[user_id]["email"],
                                   user_report_emails[user_id]["subject"],
                                   user_report_emails[user_id]["message"],
                                   None)
                del user_report_emails[user_id]
                message.reply_text("تم رفع البلاغ بنجاح.")
            else:
                message.reply_text("الرجاء الإجابة بنعم أو لا.")
        elif user_report_emails[user_id]["photo"]:
            if message.photo:
                user_report_emails[user_id]["photo"] = message.photo[-1].file_id
                send_report_thread(user_id,
                                   user_report_emails[user_id]["email"],
                                   user_report_emails[user_id]["subject"],
                                   user_report_emails[user_id]["message"],
                                   user_report_emails[user_id]["photo"])
                del user_report_emails[user_id]
                message.reply_text("تم رفع البلاغ بنجاح.")
            else:
                message.reply_text("الرجاء إرسال صورة.")
    else:
        message.reply_text("يرجى إدخال الكود للمتابعة.")

@app.on_message(filters.private & filters.user(AUTHORIZED_USER_ID))
def handle_authorized_user(client, message):
    user_id = message.from_user.id
    if user_id in authorized_user_ids:
        user_username = message.from_user.username
        if message.text == "بدء رفع البلاغات":
            user_report_emails[user_id] = {}
            message.reply_text("يرجى إرسال البريد الإلكتروني الذي سيتم منه رفع البلاغ.")
        elif message.text == "توليد كود للمطور":
            keyboard = [
                [InlineKeyboardButton("1 يوم", callback_data="1d"),
                 InlineKeyboardButton("7 أيام", callback_data="7d"),
                 InlineKeyboardButton("30 يوم", callback_data="30d")],
                [InlineKeyboardButton("إلغاء كود", callback_data="cancel_code")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            message.reply_text("يرجى اختيار مدة صلاحية الكود:", reply_markup=reply_markup)
    else:
        message.reply_text("ليس لديك الحق في استخدام هذا البوت.")

app.run()
