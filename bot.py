import logging
import os
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token (o'zingiznikini qo'ying)
TOKEN = 'YOUR_BOT_TOKEN_HERE'  # @BotFather dan oling

# Video yuklash sozlamalari
ydl_opts = {
    'format': 'best[height<=720]/best',  # 720p gacha
    'outtmpl': '%(title)s.%(ext)s',
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Assalomu alaykum! 😊\n"
        "Video yuklash uchun link yuboring (YouTube, Instagram, TikTok, Pinterest va boshqalar).\n"
        "5-30 soniyada video keladi! ⚡"
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text.strip()
    if not url.startswith(('http://', 'https://')):
        await update.message.reply_text("❌ To'g'ri link yuboring!")
        return

    await update.message.reply_text("📥 Yuklanmoqda... ⚡")

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            with yt_dlp.YoutubeDL({**ydl_opts, 'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s')}) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Video')
                file_ext = info.get('ext', 'mp4')

            # Faylni topish
            for file in os.listdir(temp_dir):
                if file.endswith(file_ext):
                    video_path = os.path.join(temp_dir, file)
                    break
            else:
                raise Exception("Fayl topilmadi!")

            # Hajm tekshiruvi (50MB dan katta bo'lsa, ogohlantirish)
            file_size = os.path.getsize(video_path) / (1024 * 1024)
            if file_size > 50:
                await update.message.reply_text("❌ Fayl katta (50MB+). Kichikroq video sinab ko'ring.")
                return

            # Video yuborish
            with open(video_path, 'rb') as video_file:
                await update.message.reply_video(
                    video=video_file,
                    caption=f"✅ {title}\nManba: {url}",
                    supports_streaming=True
                )
            await update.message.reply_text("Boshqa link yuboring! 🚀")

        except Exception as e:
            logger.error(f"Xato: {e}")
            await update.message.reply_text(f"❌ Xato: {str(e)}\nLinkni tekshiring.")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
