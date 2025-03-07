from telethon import TelegramClient
API_KEY="22341875"
API_HASH="b13c2392d55ae8a4800d3b4ed40bffb2"
#my.telegram.org adresinden alın
bot = TelegramClient('userbot',API_KEY,API_HASH)
bot.start()

#Bu komut dosyası botunuzu çalıştırmaz, sadece bir oturum oluşturur.
