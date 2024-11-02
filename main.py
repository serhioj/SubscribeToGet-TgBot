from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

import sqlite3
import csv

import os
from dotenv import load_dotenv

# Загружаем переменные среды
load_dotenv() 

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Подключаемся к базе данных SQLite и создаем таблицу, если она не существует
conn = sqlite3.connect('users_db/user_feedback.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT,
                    start_time TEXT,
                    feedback TEXT
                )''')
conn.commit()

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Множество для хранения ID пользователей, ожидающих отзыва
pending_feedback_users = set()

# Словарь для отслеживания последнего вызова команды
last_start_time = {}

# Период ожидания перед повторным вызовом команды (в секундах)
RATE_LIMIT_SECONDS = 60

@dp.message(Command("start"))
async def send_welcome(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    current_time = datetime.now()

    # Проверка на частоту вызова команды
    if user_id in last_start_time:
        last_call_time = last_start_time[user_id]
        time_since_last_call = current_time - last_call_time
        if time_since_last_call < timedelta(seconds=RATE_LIMIT_SECONDS):
            return

    # Обновляем время последнего вызова команды
    last_start_time[user_id] = current_time

    # Проверка, есть ли пользователь в базе данных
    cursor.execute("SELECT user_id FROM feedback WHERE user_id = ?", (user_id,))
    user_exists = cursor.fetchone()
    
    # Если пользователя нет в базе, добавляем его
    if not user_exists:
        start_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO feedback (user_id, username, start_time) VALUES (?, ?, ?)", (user_id, username, start_time))
        conn.commit()
    else:
        ...

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Я подписался(-ась)", callback_data="check_subscription")
    await message.answer(
        "Привет! Меня зовут Александр, и я здесь, чтобы помочь вашему бизнесу 🔥\n"
        "\nЯ готов бесплатно отдать вам гайд, <b>как привлекать ещё больше клиентов без рекламы в 2025 году.</b> "
        "Для того чтобы получить его, подпишитесь на <a href='https://t.me/defdesign'>мой телеграм-канал</a> "
        "и нажмите «Я подписался(-ась)». <b>Там правда много интересного</b> 😉",
        parse_mode="HTML", reply_markup=keyboard.as_markup()
     )

# Обработчик для проверки сообщения на пароль администратора
@dp.message(lambda message: message.text == ADMIN_PASSWORD)
async def handle_admin_password(message: Message):
    if message.text == ADMIN_PASSWORD:
        print('Сообщение совпало')
        # Генерация CSV-файла из базы данных
        cursor.execute("SELECT user_id, username, start_time, feedback FROM feedback")
        rows = cursor.fetchall()
        
        # Запись данных в CSV-файл
        csv_file_path = "user_data.csv"
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["user_id", "username", "start_time", "feedback"])
            writer.writerows(rows)
        
        # Отправка файла администратору
        await message.answer_document(FSInputFile(csv_file_path), caption="Вот файл с данными пользователей.")
    else:
        ...

@dp.callback_query(lambda c: c.data == "check_subscription")
async def check_subscription(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    member = await bot.get_chat_member(CHANNEL_ID, user_id)
    if member.status != 'left':
        await callback_query.message.edit_reply_markup(reply_markup=None)

        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="С компьютера", callback_data="from_pc")
        keyboard.button(text="С телефона", callback_data="from_mobile")
        await callback_query.message.answer(
            "Супер, вижу подписку 😎 Знаете, с вами приятно работать, поэтому забирайте файл 👇\n"
            "\nЗдесь два PDF-файла, отличающихся форматом. Выберите, с какого устройства планируете читать",
            parse_mode="HTML", reply_markup=keyboard.as_markup())
    else:
        await callback_query.message.delete()
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="Я подписался(-ась)", callback_data="retry_check_subscription")
        await callback_query.message.answer(
            "\nЯ готов бесплатно отдать вам гайд, <b>как привлекать ещё больше клиентов без рекламы в 2025 году.</b> "
            "Для того чтобы получить его, подпишитесь на <a href='https://t.me/defdesign'>мой телеграм-канал</a> "
            "и нажмите «Я подписался(-ась)». <b>Там правда много интересного</b> 😉",
            parse_mode="HTML", reply_markup=keyboard.as_markup()
        )

@dp.callback_query(lambda c: c.data == "retry_check_subscription")
async def retry_check_subscription(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    member = await bot.get_chat_member(CHANNEL_ID, user_id)
    if member.status != 'left':
        await callback_query.message.edit_reply_markup(reply_markup=None)

        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="С компьютера", callback_data="from_pc")
        keyboard.button(text="С телефона", callback_data="from_mobile")
        await callback_query.message.answer(
            "Супер, вижу подписку 😎 Знаете, с вами приятно работать, поэтому забирайте файл 👇\n"
            "\nЗдесь два PDF-файла, отличающихся форматом. Выберите, с какого устройства планируете читать",
            reply_markup=keyboard.as_markup())
    else:
        ...

@dp.callback_query(lambda c: c.data in ["from_pc", "from_mobile"])
async def send_file(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    # Проверка поля feedback для данного пользователя
    cursor.execute("SELECT feedback FROM feedback WHERE user_id = ?", (user_id,))
    feedback = cursor.fetchone()
    
    if callback_query.data == "from_pc":
        await callback_query.message.edit_reply_markup(reply_markup=None)
        document = FSInputFile("files_to_get/guide_for_pc.pdf")
        await callback_query.message.answer_document(document)
    elif callback_query.data == "from_mobile":
        await callback_query.message.edit_reply_markup(reply_markup=None)
        document = FSInputFile("files_to_get/guide_for_mobile.pdf")
        await callback_query.message.answer_document(document)
    
    # Запускаем задачу для отложенного сообщения про статью
        asyncio.create_task(send_delayed_article(user_id))

    # Если поле feedback пустое (None), запускаем задачу для отложенного сообщения
    if feedback is None or feedback[0] is None:
        # Запускаем задачу для отложенного сообщения
        asyncio.create_task(send_delayed_message(user_id))

async def send_delayed_message(user_id: int):
    await asyncio.sleep(60 * 60)
    try:
        pending_feedback_users.add(user_id)
        
        await bot.send_message(
            user_id,
            "Привет,👋 как вам гайд? Расскажите подробнее о своём впечатлении, мне важно знать, что я делюсь качественным продуктом 🤝"
        )

    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

async def send_delayed_article(user_id: int):
    await asyncio.sleep(60 * 90)
    try:
        pending_feedback_users.add(user_id)
        
        await bot.send_message(
            user_id,
            "📉 Часто предприниматели теряют своих клиентов, добавляя на главный экран слоган вместо УТП. "
            "В итоге это приводит к тому, что потенциальные клиенты не понимают свою выгоду и покидают ресурс. "
            "Чтобы этого не происходило, доносите пользу вашего продукта сразу. Например, вместо «Мама, папа, я – танцевальная семья!» "
            "напишите «Индивидуальные занятия по танцам для начинающих взрослых и детей от 6 лет, без лишних глаз».\n"
            "\n🫠 Таких незаметных ошибок целое море. Я собрал 6 самых распространённых ошибок в одну "
            "<a href='https://tenchat.ru/media/2555890-ubiytsy-konversii-6-antagonistov-prodayuschego-sayta?clckid=8780e6b5'>короткую статью, которая поможет вам добиться максимальных показателей конверсии.</a>"
            " Если интересно — буду рад вашему вниманию."
        )   
    except Exception as e:
        print(f"Ошибка при отправке статьи: {e}")

@dp.message()
async def save_feedback(message: Message):
    user_id = message.from_user.id
    if user_id in pending_feedback_users:
        username = message.from_user.username
        feedback = message.text
        cursor.execute("UPDATE feedback SET feedback = ? WHERE user_id = ?", (feedback, user_id))
        conn.commit()
        
        pending_feedback_users.remove(user_id)
        
        await message.answer("Спасибо за ваш отзыв!")



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
