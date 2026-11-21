import os
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

LESSONS = {
    1: {"text": "📚 *1-КҮН: Вайбкодинг деген эмне?*\n\nВайбкодинг = Код жазбай, AI менен сүйлөшүп программа жасоо.\n\nСен — директорсуң, AI — программист.\n\n❌ Жаман: 'Мага сайт жаса'\n✅ Жакшы: 'Мага футбол тууралуу кооз сайт жаса. Фону кара болсун'\n\n*Тапшырма:* AI'га 'Мага өзүм жөнүндө кыска текст жаз' деп жаз.",
        "video": "https://www.youtube.com/results?search_query=вайб+кодинг+с+нуля",
        "video_name": "🎥 Видео: Вайб-кодинг нөлдөн"},
    2: {"text": "📚 *2-КҮН: Туура промп жазуу*\n\nПромптун 3 сыры:\n1. *Эмне* керек? - Сайт, бот, оюн\n2. *Кандай* болсун? - Түсү, стили\n3. *Мисал* бер - 'Инстаграмдай болсун'\n\n*Тапшырма:* 'Мага Реал Мадрид күйөрмандары үчүн сайт жаса' деп жаз.",
        "video": "https://www.youtube.com/results?search_query=vibe+coding+tutorial+beginners",
        "video_name": "🎥 Видео: Туура промп"},
    3: {"text": "📚 *3-КҮН: Биринчи сайтың*\n\nAI'га: 'Мага HTML менен жөнөкөй сайт жаса. Атым... Хоббим футбол'\n\n*Тапшырма:* Өзүңдүн визитка-сайтыңды жаса.",
        "video": "https://www.youtube.com/results?search_query=build+first+website+vibe+coding",
        "video_name": "🎥 Видео: Биринчи сайт"},
    4: {"text": "📚 *4-КҮН: AI менен бот жасоо*\n\nAI'га: 'Мага Telegram боттун кодун жаз. /start басса салам айтсын' деп жаз.",
        "video": "https://www.youtube.com/results?search_query=вайбкодинг+телеграм+бот",
        "video_name": "🎥 Видео: Бот жасоо"},
    5: {"text": "📚 *5-КҮН: Катаны оңдоо*\n\nКата чыкса коркпо! AI'га жибер: 'Ушундай ката чыкты, оңдоп берчи'",
        "video": "https://www.youtube.com/results?search_query=vibe+coding+debugging",
        "video_name": "🎥 Видео: Катаны оңдоо"},
    6: {"text": "📚 *6-КҮН: Өз идеяң*\n\nЭң жакшы идеялар жашоодон чыгат. Мисалы: дүкөн үчүн бот, сабак үйрөткөн бот.\n\n*Тапшырма:* 3 идея ойлоп тап.",
        "video": "https://www.youtube.com/results?search_query=vibe+coding+idea+to+app",
        "video_name": "🎥 Видео: Идеядан колдонмого"},
    7: {"text": "📚 *7-КҮН: Финал!*\n\nКуттуктайм! Сен эми вайбкодерсиң 🎉\n\nЭми өз проектиңди жасап, досторуңа көрсөт.",
        "video": "https://www.youtube.com/results?search_query=how+to+start+vibe+coding",
        "video_name": "🎥 Видео: Толук курс"},
}

users = {}

def get_keyboard(day):
    lesson = LESSONS[day]
    keyboard = [[InlineKeyboardButton(lesson["video_name"], url=lesson["video"])]]
    nav = []
    if day > 1:
        nav.append(InlineKeyboardButton("⬅️ Мурунку", callback_data=f"lesson_{day-1}"))
    if day < 7:
        nav.append(InlineKeyboardButton("Кийинки ➡️", callback_data=f"lesson_{day+1}"))
    if nav:
        keyboard.append(nav)
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in users:
        users[chat_id] = 1
    keyboard = [[InlineKeyboardButton("🚀 Сабакты баштоо", callback_data="lesson_1")],
                [InlineKeyboardButton("🔔 Күнүнө сабакты күйгүзүү", callback_data="subscribe")]]
    await update.message.reply_text("Салам! Мен *Вайбкодинг Мугалимим* 🤖🇰🇬\n\nКүнүнө саат 10:00дө сабак жиберип турам.", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Катталдың! ✅")
    await query.edit_message_text("🔔 Сонун! Эртең саат 10:00дө сабагың келет. ⏰")

async def show_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    day = int(query.data.split("_")[1])
    users[query.message.chat_id] = day
    await query.answer()
    await query.edit_message_text(LESSONS[day]["text"], parse_mode="Markdown", reply_markup=get_keyboard(day))

async def send_daily_lesson(context: ContextTypes.DEFAULT_TYPE):
    for chat_id, day in list(users.items()):
        if day > 7: continue
        try:
            await context.bot.send_message(chat_id=chat_id, text=f"⏰ *Бүгүнкү сабагың даяр!*\n\n{LESSONS[day]['text']}", parse_mode="Markdown", reply_markup=get_keyboard(day))
            users[chat_id] = day + 1
        except: pass

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(show_lesson, pattern="^lesson_"))
app.add_handler(CallbackQueryHandler(subscribe, pattern="^subscribe"))
app.job_queue.run_daily(send_daily_lesson, time=datetime.time(hour=4, minute=0, second=0))
app.run_polling()