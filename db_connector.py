import os
import sys
import django
import dotenv
sys.path.append(os.path.join(os.getcwd(), "gatekeeper_webapp"))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gatekeeper_webapp.config.settings')
dotenv.read_dotenv()
django.setup()
sys.path.append(os.path.join(os.getcwd(), "telegram_bot"))
