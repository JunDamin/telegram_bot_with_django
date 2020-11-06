import os
import sys
import django
import dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
dotenv.read_dotenv()
django.setup()
sys.path.append(os.path.join(os.getcwd(), "telegram_bot"))


from telegram_bot.telegram_bot import main
main()
# import script