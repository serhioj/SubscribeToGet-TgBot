# SubscribeToGet-TgBot

## Description

This is a Telegram bot designed to attract clients without advertising. The bot offers users a guide on how to increase the number of clients. Users can receive the guide by subscribing to the channel and providing feedback on the received information.

## Features

- Subscription check for the channel
- Sending guides in PDF format
- Saving user feedback in the database
- Generating a CSV file with user data for the administrator
- Automatic reminders sent to users

## Installation

1. Clone the repository:

        git clone https://github.com/Your_Username/Owner-avatar-SubscribeToGet-TgBot.git

2. Navigate to the project directory:

        cd Owner-avatar-SubscribeToGet-TgBot

3. Install the required dependencies:

        pip install -r requirements.txt

4. Create a .env file in the root directory and add the following variables:

        TOKEN=your_bot_token
        CHANNEL_ID=channel_id
        ADMIN_PASSWORD=admin_password

5. Run the bot:

        python main.py

## Usage

Send the /start command to begin interacting with the bot.
Subscribe to the specified channel and send "I subscribed" to receive the guide.
After receiving the guide, you can leave your feedback.


# SubscribeToGet-TgBot

## Описание

Это Telegram-бот, разработанный для привлечения клиентов без рекламы. Бот предлагает пользователям скачать гайд о том, как увеличивать количество клиентов. Пользователи могут получить гайд, подписавшись на канал и отправив отзыв о полученной информации.

### Возможности

- Проверка подписки на канал
- Отправка гайдов в формате PDF
- Сохранение отзывов пользователей в базе данных
- Генерация CSV-файла с данными пользователей для администратора
- Автоматическая отправка напоминаний пользователям


## Установка

1. Склонируйте репозиторий:

        git clone https://github.com/Ваш_Пользователь/SubscribeToGet-TgBot.git

2. Перейдите в директорию проекта:

        cd Owner-avatar-SubscribeToGet-TgBot

3. Установите необходимые зависимости:

        pip install -r requirements.txt

4. Создайте файл .env в корневой директории и добавьте туда следующие переменные:

        TOKEN=ваш_токен_бота
        CHANNEL_ID=идентификатор_канала_для_подписки
        ADMIN_PASSWORD=пароль_для_администратора

5. Запустите бота:

        python main.py

## Использование

Отправьте команду /start, чтобы начать взаимодействие с ботом.
Подпишитесь на указанный канал и отправьте "Я подписался(-ась)", чтобы получить гайд.
После получения гайда вы можете оставить свой отзыв.
