from telegram.ext import ApplicationBuilder
import Start

def main():
    app = ApplicationBuilder().token("7635460313:AAEoI1tww8TEGV1ObWK9qvyXWSf-WhiMXTQ").build()

    # Подключаем handlers
    app.add_handler(Start.conv_handler)

    app.run_polling()

if __name__ == "__main__":
    main()