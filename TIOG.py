import telebot
from telebot import types
import sqlite3
import json

bot = telebot.TeleBot("8194023558:AAHVlbIPSv2ExcB8ZBg4nCl3XYBB2U5zf4g")

conn = sqlite3.connect('bot_database.db', check_same_thread=False)
cursor = conn.cursor()


# Создаем таблицу с проверкой существующих столбцов
def init_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        score INTEGER DEFAULT 0,
        best_score INTEGER DEFAULT 0
    )
    ''')

    # Проверяем существование столбца best_score
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'best_score' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN best_score INTEGER DEFAULT 0')

    conn.commit()


init_db()


def register_user(user_id, username):
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (id, username, score, best_score) VALUES (?, ?, 0, 0)", (user_id, username))
        conn.commit()

'''
def update_score(user_id, additional_points):
    cursor.execute("SELECT score FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        new_score = result[0] + additional_points
        cursor.execute("UPDATE users SET score = ? WHERE id = ?", (new_score, user_id))
        conn.commit()

'''
def get_ratings():
    cursor.execute("SELECT username, best_score FROM users ORDER BY best_score DESC LIMIT 10")
    return cursor.fetchall()


def update_best_score(user_id, new_score):
    cursor.execute("SELECT best_score FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    if result and new_score > result[0]:
        cursor.execute(
            "UPDATE users SET best_score = ? WHERE id = ?",
            (new_score, user_id)
        )
        conn.commit()

def get_games_markup():
    """Основная клавиатура с кнопками"""
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    english_web_app = types.WebAppInfo(url="https://arinauru.github.io/english_game.html")

    btn_english = types.KeyboardButton("Игра: Английский", web_app=english_web_app)
    btn_rating = types.KeyboardButton("Рейтинг")

    # чтобы не вызывать ошибку
    # flappy_web_app = types.WebAppInfo(url="https://YOUR_DOMAIN/flappy_birds.html")
    # pingpong_web_app = types.WebAppInfo(url="https://YOUR_DOMAIN/ping_pong.html")
    # btn_flappy = types.KeyboardButton("Flappy Birds", web_app=flappy_web_app)
    # btn_pingpong = types.KeyboardButton("Ping-Pong", web_app=pingpong_web_app)

    # markup.add(btn_english, btn_flappy, btn_pingpong, btn_rating)
    markup.add(btn_english, btn_rating)
    return markup


def get_english_games_markup():
    """Инлайн-клавиатура с выбором типа игры"""
    markup = types.InlineKeyboardMarkup(row_width=1)

    # Создаем кнопки для разных игр
    snake_game = types.InlineKeyboardButton(
        text="🐍 Грамматическая Змейка",
        web_app=types.WebAppInfo(url="https://arinauru.github.io/english_game.html")
    )
    markup.add(snake_game)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    register_user(message.from_user.id, message.from_user.username)
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Выберите игру или просмотрите рейтинг:",
        reply_markup=get_games_markup()
    )


@bot.message_handler(func=lambda message: message.text == "🎮 Игра: Английский")
def show_english_games(message):
    """Обработчик кнопки выбора английских игр"""
    bot.send_message(
        message.chat.id,
        "📚 Выберите тип задания:",
        reply_markup=get_english_games_markup()
    )


@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.strip()
    if text == "Рейтинг":
        ratings = get_ratings()
        if ratings:
            rating_text = "🏆 Топ лучших результатов 🏆\n\n"
            for i, (username, best_score) in enumerate(ratings, 1):
                rating_text += f"{i}. {username} — {best_score} очков\n"
        else:
            rating_text = "Рейтинг пока пуст."
        bot.send_message(message.chat.id, rating_text)
    else:
        bot.send_message(message.chat.id, "Выберите игру из меню или просмотрите рейтинг.")


@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        data = message.web_app_data.data
        result = json.loads(data)

        if result.get("bestScore"):
            update_best_score(message.from_user.id, result["bestScore"])
            bot.send_message(
                message.chat.id,
                f"Ваш новый рекорд: {result['bestScore']} очков!"
            )
    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "Ошибка при обработке данных игры")


@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        data = message.web_app_data.data
        result = json.loads(data)

        if result.get("bestScore"):
            update_best_score(message.from_user.id, result["bestScore"])
            bot.send_message(
                message.chat.id,
                f"Ваш новый рекорд: {result['bestScore']} очков!"
            )
    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "Ошибка при обработке данных игры")

bot.polling(none_stop=True, interval=0)
