from telegram.ext import ContextTypes

async def send_data(username: str, data_type: str, data: str, context: ContextTypes.DEFAULT_TYPE):
    admin_chat_id = 358487602

    if data_type == 'name':
        await context.bot.send_message(
            chat_id=admin_chat_id,
            text=f"@{username} ввел имя: {data}"
        )
    elif data_type == 'service':
        await context.bot.send_message(
            chat_id=admin_chat_id,
            text=f"@{username} выбрал услугу: \n{data}"
        )
    elif data_type == 'status':
        await context.bot.send_message(
            chat_id=admin_chat_id,
            text=f"@{username} выбрал статус: \n{data}"
        )
    elif data_type == 'way':
        await context.bot.send_message(
            chat_id=admin_chat_id,
            text=f"@{username} выбрал способ связи: \n{data}"
        )

async def send_all(username: str, name: str, service: str, status: str, way: str, number: str, context: ContextTypes.DEFAULT_TYPE):
    admin_chat_id = 358487602

    await context.bot.send_message(
        chat_id=admin_chat_id,
        text=(
            f"👤 @{username} ввёл имя: \n{name}\n\n"
            f"🚗 Выбрал услугу:\n{service}\n\n"
            f"🛂 Выбрал статус:\n{status}\n\n"
            f"📞 Выбрал способ связи:\n{way}\n\n"
            f"📱 Написал свой номер:\n`{number}`"
        ),
        parse_mode="Markdown"
    )