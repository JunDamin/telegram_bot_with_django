import os
import sys
import django
import dotenv
# from telegram_bot.telegram_bot import main

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
dotenv.read_dotenv()
django.setup()
sys.path.append(os.path.join(os.getcwd(), "telegram_bot"))


# main()
import script