import telebot
from telebot import types

TOKEN = "7985957320:AAGNlTzAR7YLVEK_QMXJo8FWGotNbRF7VlE"
ADMIN_ID = 8693972785

bot = telebot.TeleBot(TOKEN)

user_mode = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    b1 = types.KeyboardButton("🛒 Купить приват")
    b2 = types.KeyboardButton("📹 Скинуть видео контент")
    b3 = types.KeyboardButton("🛠 Поддержка")
    b4 = types.KeyboardButton("📩 Связь с админом")

    markup.add(b1)
    markup.add(b2)
    markup.add(b3)
    markup.add(b4)

    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать!\n\nВыберите нужный пункт меню.",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: m.text == "🛒 Купить приват")
def buy(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("1️⃣ Dark Ebelex — 1300₽")
    markup.add("2️⃣ Darkness Chechnya — 1200₽ VIP")
    markup.add("3️⃣ Темный Кавказ — 1000₽ VIP")
    markup.add("4️⃣ Покрытые — 1000₽ VIP")
    markup.add("5️⃣ Rachid X — 600₽ VIP")
    markup.add("⬅ Назад")

    bot.send_message(
        message.chat.id,
        "Выберите приват:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: m.text == "⬅ Назад")
def back(message):
    start(message)


@bot.message_handler(func=lambda m: m.text in [
    "1️⃣ Dark Ebelex — 1300₽",
    "2️⃣ Darkness Chechnya — 1200₽ VIP",
    "3️⃣ Темный Кавказ — 1000₽ VIP",
    "4️⃣ Покрытые — 1000₽ VIP",
    "5️⃣ Rachid X — 600₽ VIP"
])
def product(message):
    bot.send_message(
        message.chat.id,
        f"Вы выбрали:\n\n{message.text}\n\n"
        "⏳ Для покупки привата напишите в поддержку бота .\n"
        "Названия выбранного вами привата для покупки .\n\n"
        "Далее ожидайте ответ  ❤️"
    )

@bot.message_handler(func=lambda m: m.text == "📹 Скинуть видео контент")
def video(message):
    user_mode[message.chat.id] = "Видео"

    bot.send_message(
        message.chat.id,
        "Спасибо, что решили поделиться с нами контентом для наших приватных каналов. Мы очень это ценим!\n\n"
        "Пришлите видео, которое в дальнейшем мы сможем опубликовать.\n\n"
        "❤️ С любовью, Ebelex."
    )


@bot.message_handler(func=lambda m: m.text == "🛠 Поддержка")
def support(message):
    user_mode[message.chat.id] = "Поддержка"

    bot.send_message(
        message.chat.id,
        "Это служба поддержки канала Ebelex.\n\n"
        "Задайте свой вопрос, и мы ответим вам как можно скорее."
    )


@bot.message_handler(func=lambda m: m.text == "📩 Связь с админом")
def admin(message):
    user_mode[message.chat.id] = "Админ"

    bot.send_message(
        message.chat.id,
        "Все следующие сообщения будут отправлены администраторам.\n"
        "Спасибо за понимание."
    )


@bot.message_handler(content_types=['video'])
def get_video(message):
    if message.chat.id in user_mode:
        bot.send_message(
            ADMIN_ID,
            f"📹 Видео\n"
            f"От: {message.from_user.first_name}\n"
            f"ID: {message.from_user.id}\n"
            f"Раздел: {user_mode[message.chat.id]}"
        )

        bot.forward_message(
            ADMIN_ID,
            message.chat.id,
            message.message_id
        )

        bot.send_message(
            message.chat.id,
            "✅ Видео отправлено администрации."
        )


@bot.message_handler(func=lambda m: True)
def all_messages(message):
    if message.chat.id in user_mode:

        bot.send_message(
            ADMIN_ID,
            f"💬 Новое сообщение\n\n"
            f"👤 {message.from_user.first_name}\n"
            f"🆔 {message.from_user.id}\n"
            f"📂 {user_mode[message.chat.id]}\n\n"
            f"{message.text}"
        )

        bot.send_message(
            message.chat.id,
            "✅ Ваше сообщение отправлено администрации."
        )


print("Бот запущен...")

bot.infinity_polling()

