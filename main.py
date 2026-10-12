import telebot

# Сіз берген токен орнатылды
TOKEN = '8787346659:AAEGhjG9VxdmAs6c8s-_ZEzKg_pWC59VE7w'
bot = telebot.TeleBot(TOKEN)

# Телефондар базасы (Модель: [Дюйм, Герц])
PHONE_DATABASE = {
    "redmi note 10": [6.43, 60],
    "redmi note 11": [6.43, 90],
    "poco x3 pro": [6.67, 120],
    "samsung a52": [6.5, 90],
    "iphone 11": [6.1, 60],
    "iphone 13": [6.1, 60],
    "iphone 13 pro": [6.1, 120],
    "samsung a32": [6.4, 90],
    "poco x4 pro": [6.67, 120],
    "redmi note 12": [6.67, 120]
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        "🎮 **Free Fire Настройка Ботқа қош келдіңіз!**\n\n"
        "Телефоныңыздың маркасы мен моделін жазыңыз (мысалы: `Poco X3 Pro` немесе `Redmi Note 10`), "
        "мен сізге схема бойынша настройка шығарып беремін!"
    )

@bot.message_handler(func=lambda message: True)
def calculate_settings(message):
    phone_name = message.text.lower().strip()
    
    # Базадан іздеу
    phone_info = PHONE_DATABASE.get(phone_name)
    
    if not phone_info:
        # Егер базада болмаса, орташа стандартты мән аламыз (6.5 дюйм, 60 Гц)
        inch = 6.5
        hz = 60
    else:
        inch, hz = phone_info
        
    # 1. Чувствительность (Обзор) есебі (60Гц үшін ~185, 90-120Гц үшін ~170)
    if hz <= 60:
        sens = "185"
    else:
        sens = "170"
        
    # 2. DPI есебі (Формула: (Дюйм + 1.6) * 71)
    calculated_dpi = round((inch + 1.6) * 71, 1)
    
    # 3. Кнопка огня есебі (Дюймге қарай)
    if inch > 6.5:
        btn_size = "42% - 44% (Үлкен экран үшін кішірейтілді)"
    elif inch < 6.2:
        btn_size = "50% - 53% (Кіші экран үшін үлкейтілді)"
    else:
        btn_size = "45% - 48% (Орташа өлшем)"

    # Нәтиже
    result_text = (
        f"🎯 **ТЕЛЕФОН НАСТРОЙКАСЫ**\n"
        f"📱 Модель: **{message.text.title()}** ({inch} дюйм, {hz} Hz)\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🔥 **Чувствительность (Обзор):** {sens}\n"
        f"⚙️ **DPI:** `{calculated_dpi}`\n"
        f"   *(Формула: ({inch} + 1.6) * 71 = {calculated_dpi})*\n"
        f"🎯 **Кнопка огня:** {btn_size}\n\n"
        f"💡 *Схема бойынша арнайы есептелді!*"
    )
    
    bot.send_message(message.chat.id, result_text, parse_mode="Markdown")

print("Бот сәтті іске қосылды және жұмыс істеп тұр...")
bot.infinity_polling()
