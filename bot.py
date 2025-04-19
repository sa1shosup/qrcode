import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Функция генерации изображения с QR
def generate_ticket_image(
    qr_data, booking_number, checkpoint, date, time_range,
    vehicle_plate, trailer_plate, country, print_time
):
    qr = qrcode.make(qr_data).resize((400, 400))
    img = Image.new("RGB", (1000, 600), "white")
    draw = ImageDraw.Draw(img)

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 20)
    small_font = ImageFont.truetype(font_path, 16)
    bold_font = ImageFont.truetype(font_path, 24)

    img.paste(qr, (50, 100))

    draw.text((500, 30), "ВЫПИСКА ИЗ СИСТЕМЫ\nЭЛЕКТРОННОЙ ОЧЕРЕДИ", font=bold_font, fill="black")
    draw.text((500, 80), f"Дата и время распечатки: {print_time}", font=small_font, fill="gray")
    draw.text((500, 120), "БРОНИРОВАНИЕ", font=font, fill="black")
    draw.text((500, 150), f"Статус: В очереди", font=small_font, fill="purple")
    draw.text((500, 180), f"№ бронирования: {booking_number}", font=small_font, fill="black")
    draw.text((500, 210), f"Пункт пропуска: {checkpoint}", font=small_font, fill="black")
    draw.text((500, 240), f"Дата: {date}", font=small_font, fill="black")
    draw.text((500, 270), f"Ориентировочное время: {time_range}", font=small_font, fill="black")
    draw.text((500, 300), f"Тип очереди: Выбранное время", font=small_font, fill="black")
    draw.text((500, 340), "ТРАНСПОРТ", font=font, fill="black")
    draw.text((500, 370), f"Номерной знак транспорта: {vehicle_plate}", font=small_font, fill="black")
    draw.text((500, 400), f"Номерной знак прицепа: {trailer_plate}", font=small_font, fill="black")
    draw.text((500, 430), f"Страна регистрации: {country}", font=small_font, fill="black")
    draw.text((50, 510), "Для подтверждения бронирования\nпредъявите QR для сканирования на пункте пропуска", font=small_font, fill="black")

    file_path = "ticket.png"
    img.save(file_path)
    return file_path

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь команду /ticket чтобы получить талон.")

# Команда /ticket
async def ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_path = generate_ticket_image(
        qr_data="https://example.com",
        booking_number="A334BESCF0368C",
        checkpoint="Нур Жолы - Хоргос",
        date="04.03.2025",
        time_range="21:00–22:00",
        vehicle_plate="931AFY13",
        trailer_plate="97AGJ13",
        country="Казахстан",
        print_time="04.03.2025 14:39"
    )
    await update.message.reply_photo(photo=open(image_path, 'rb'))

# Запуск
if __name__ == "__main__":
    TOKEN = os.environ["TOKEN"]  # Токен из переменных окружения
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ticket", ticket))
    print("Бот запущен...")
    app.run_polling()
