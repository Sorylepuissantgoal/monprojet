import sys
import os
import django

# Initialise Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Crée le superutilisateur s’il n’existe pas déjà
if not User.objects.filter(username='CAMARA').exists():
    User.objects.create_superuser('CAMARA', 'IBRAHIMASORYCAMARA3174@GMAIL.COM', 'CAMARA1813d')
    print("✅ Superutilisateur créé.")
else:
    print("⚠️ Superutilisateur existe déjà.")

