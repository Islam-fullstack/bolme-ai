# Bólmede — Adam Háreketiniń Dawamlılıǵın Bahalaw

Django + SQLite + OpenRouter AI asosida qurilgan harakat davomiyligini baholash tizimi.

## O'rnatish

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Sozlash

`.env` faylini tahrirlang:
```
DJANGO_SECRET_KEY=tasodifiy-maxfiy-kalit
OPENROUTER_API_KEY=siz-ni-openrouter-kalitingiz
OPENROUTER_MODEL=qwen/qwen3-5-flash-02-23
```

## Ishga tushirish

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Brauzerda `http://127.0.0.1:8000` ga kiring.

## Admin panel

`http://127.0.0.1:8000/admin/` — superuser bilan kiring.
