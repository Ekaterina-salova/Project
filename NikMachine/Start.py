from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (MessageHandler, filters, CommandHandler,
    CallbackQueryHandler, ConversationHandler, ContextTypes)
import re
from Send_sms import send_data, send_all

NAME, SERVICE, STATUS, WAY, NUMBER = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.from_user is not None:
        user = update.message.from_user.id
        username = update.message.from_user.username or "без username"

        admin_chat_id = 358487602
        await context.bot.send_message(
            chat_id=admin_chat_id,
            text=f"Новый пользователь начал чат:\n"
                 f"ID: {user}\n"
                 f"Username: @{username}"
        )

        await update.message.reply_text("Здравствуйте! Представьтесь, пожалуйста (имя и фамилия):"
            "(Например: Иван Петров)")
        return NAME
        


async def check_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None or context.user_data is None:
        return ConversationHandler.END
    
    name = update.message.text.strip()
    if update.message.from_user is None:
        return ConversationHandler.END
    username = update.message.from_user.username or "без username"
    await send_data(username, 'name', name, context)
    parts = name.split()
    
    if len(parts) > 1:
        first_name = parts[0]
    else:
        first_name = name

    context.user_data["name"] = name
    context.user_data["first_name"] = first_name
    keyboard = [
        [InlineKeyboardButton("🚗 Подбор автомобиля", callback_data="car_selection")],
        [InlineKeyboardButton("🚙 Подбор + выезд на осмотр", callback_data="check_out")],
        [InlineKeyboardButton("📝 Помощь с оформлением автомобиля", callback_data="car_registration")],
        [InlineKeyboardButton("💼 Консультация по автофинансам", callback_data="consultation")],
        [InlineKeyboardButton("❓ Другое", callback_data="other")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"Благодарю вас, {first_name}! \nЧем я могу вам помочь?",
                                    reply_markup=reply_markup)
    return SERVICE
    


async def check_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return ConversationHandler.END
    if context.user_data is None:
        return ConversationHandler.END
    user = query.from_user
    if user is None:
        return ConversationHandler.END
    username = user.username or "без username"
    

    await query.answer()

    if query.data == "car_selection":
        context.user_data["service"] = 'Подбор автомобиля'
        await send_data(username, 'service', 'Подбор автомобиля', context)
    elif query.data == "check_out":
        context.user_data["service"] = 'Подбор + выезд на осмотр'
        await send_data(username, 'service', 'Подбор + выезд на осмотр', context)
    elif query.data == "car_registration":
        context.user_data["service"] = 'Помощь с оформлением автомобиля'
        await send_data(username, 'service', 'Помощь с оформлением автомобиля', context)
    elif query.data == "consultation":
        context.user_data["service"] = 'Консультация по страхованию, лизингу или кредиту'
        await send_data(username, 'service', 'Консультация по страхованию, лизингу или кредиту', context)
    elif query.data == "other":
        context.user_data["service"] = 'Другое'
        await send_data(username, 'service', 'Другое', context)

    keyboard = [
        [InlineKeyboardButton("🆘 Беженец", callback_data="refugee")],
        [InlineKeyboardButton("📄 ВНЖ (учёба, работа, живность)", callback_data="vnz")],
        [InlineKeyboardButton("🏠 ПМЖ", callback_data="pmz")],
        [InlineKeyboardButton("🛡️ Гражданство", callback_data="citizenship")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("Уточните, пожалуйста, ваш статус в Словакии / ЕС:",
                                  reply_markup=reply_markup)
    return STATUS
    


async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return ConversationHandler.END
    if context.user_data is None:
        return ConversationHandler.END
    user = query.from_user
    if user is None:
        return ConversationHandler.END
    username = user.username or "без username"

    await query.answer()

    if query.data == "refugee":
        context.user_data["status"] = 'Беженец'
        await send_data(username, 'status', 'Беженец', context)
    elif query.data == "vnz":
        context.user_data["status"] = 'ВНЖ (учёба, работа, живность)'
        await send_data(username, 'status', 'ВНЖ (учёба, работа, живность)', context)
    elif query.data == "pmz":
        context.user_data["status"] = 'ПМЖ'
        await send_data(username, 'status', 'ПМЖ', context)
    elif query.data == "citizenship":
        context.user_data["status"] = 'Гражданство'
        await send_data(username, 'status', 'Гражданство', context)

    keyboard = [
        [InlineKeyboardButton("💬 Сообщение в Telegram / WhatsApp", callback_data="telegram")],
        [InlineKeyboardButton("📞 Телефонный звонок", callback_data="call")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("Какой способ связи для вас предпочтительнее?",
                                  reply_markup=reply_markup)
    return WAY
    


async def check_way(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return ConversationHandler.END
    if context.user_data is None:
        return ConversationHandler.END
    user = query.from_user
    if user is None:
        return ConversationHandler.END
    username = user.username or "без username"

    await query.answer()

    if query.data == "telegram":
        context.user_data["way"] = 'Сообщение в Telegram / WhatsApp'
        await send_data(username, 'way', 'Сообщение в Telegram / WhatsApp', context)
    elif query.data == "call":
        context.user_data["way"] = 'Телефонный звонок'
        await send_data(username, 'way', 'Телефонный звонок', context)

    await query.edit_message_text(
            "Укажите, пожалуйста, ваш номер телефона, чтобы мы могли с вами связаться.\n" 
            "Пример: `+4219xxxxxxxx`.",
            parse_mode="Markdown")
    return NUMBER
    


async def check_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None or context.user_data is None:
        return ConversationHandler.END
    if update.message.from_user is None:
        return ConversationHandler.END
    username = update.message.from_user.username or "без username"

    number = update.message.text.strip()

    if not re.fullmatch(r"\+\d{10,12}", number):
        await update.message.reply_text(
            "❌ Пожалуйста, введите корректный номер телефона в международном формате.\n"
            "Например: `+421912345678`",
            parse_mode="Markdown"
        )
        return NUMBER

    first_name = context.user_data.get("first_name")
    name = context.user_data.get("name")
    service = context.user_data.get("service")
    status = context.user_data.get("status")
    way = context.user_data.get("way")
    await send_all(username, str(name), str(service), str(status), str(way), number, context)

    await update.message.reply_text(f"✅ Спасибо за вашу заявку, {first_name}!\n"
                                    "Мы свяжемся с вами в ближайшее время.\n"
                                    "Если хотите оставить ещё одну заявку, введите команду /start.")
    return ConversationHandler.END
    

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_name)],
        SERVICE: [CallbackQueryHandler(check_service, pattern=r"^(car_selection|check_out|car_registration|consultation|other)$")],
        STATUS: [CallbackQueryHandler(check_status, pattern=r"^(refugee|vnz|pmz|citizenship)$")],
        WAY: [CallbackQueryHandler(check_way, pattern=r"^(telegram|call)$")],
        NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_number)],
    },
    fallbacks=[],
    per_message=False
)