import os
import sys
import django
import dotenv
sys.path.append(os.path.join(os.getcwd(), "backend"))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')
dotenv.read_dotenv()
django.setup()
sys.path.append(os.path.join(os.getcwd(), "telegram_bot"))
