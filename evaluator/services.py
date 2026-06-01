import requests
import json
from django.conf import settings


def ai_tahlil_qil(ma_lumot: dict) -> tuple[str, float]:
    """
    Send movement data to OpenRouter AI and get analysis + score.
    Returns (tahlil_matni, baho_0_100)
    """
    prompt = f"""Siz sport va jismoniy faollik bo'yicha mutaxassis sun'iy intellektsiz.
Quyidagi sport faoliyati ma'lumotlarini tahlil qiling va O'zbek tilida javob bering.

Ma'lumotlar:
- Ism: {ma_lumot['ism']} {ma_lumot['familiya']}
- Yosh: {ma_lumot['yosh']} yil
- Harakat turi: {ma_lumot['harakat_turi']}
- Daraja: {ma_lumot['daraja']}
- Davomiylik: {ma_lumot['davomiylik_daqiqa']} daqiqa
- Masofa: {ma_lumot['masofa_km']} km
- Yurak urishi: {ma_lumot['yurak_urishi']} urish/daqiqa
- Izoh: {ma_lumot.get('izoh', 'Yo\'q')}

Iltimos, quyidagi formatda tahlil qiling:

1. **Umumiy baholash**: Faoliyatning qisqacha baholash (2-3 gap)
2. **Kuchli tomonlar**: Nima yaxshi bajarilgan
3. **Takomillashtirish uchun tavsiyalar**: Aniq va amaliy maslahatlar
4. **Xavf omillari**: Mavjud bo'lsa, sog'liq uchun xavflar
5. **Keyingi maqsad**: Qisqa muddatli maqsad tavsiyasi

Tahlil oxirida 0 dan 100 gacha bo'lgan son ko'rsating: BAHO: [son]
(Baho faqat son bo'lsin, masalan: BAHO: 78)"""

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Bolmede Harakat Baholash",
    }

    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1200,
        "temperature": 0.7,
    }

    try:
        resp = requests.post(
            settings.OPENROUTER_BASE_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        tahlil = data["choices"][0]["message"]["content"].strip()

        # Extract score
        baho = 50.0
        for line in tahlil.split("\n"):
            if "BAHO:" in line:
                try:
                    baho = float(line.split("BAHO:")[-1].strip().replace(",", "."))
                    baho = max(0, min(100, baho))
                except ValueError:
                    pass

        return tahlil, baho

    except requests.exceptions.RequestException as e:
        return f"AI tahlili amalga oshmadi: {str(e)}", 0.0
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return f"Javob qayta ishlashda xato: {str(e)}", 0.0
