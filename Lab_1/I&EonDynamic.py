import re
import math
import requests # pip install requests
from collections import Counter
from bs4 import BeautifulSoup # pip install beautifulsoup4


def get_text_from_url(url):
    try:
        # Відправляємо запит на сайт
        headers = {'User-Agent': 'Mozilla/5.0'}  # Додаємо "ім'я" браузера, щоб сайт не блокував запит
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Перевірка, чи вдалося завантажити сторінку

        # Очищаємо вміст від HTML-тегів
        soup = BeautifulSoup(response.text, 'html.parser')

        # Видаляємо непотрібні елементи (скрипти, стилі, рекламу тощо)
        for script_or_style in soup(["script", "style", "header", "footer", "nav"]):
            script_or_style.decompose()

        # Отримуємо чистий текст
        clean_text = soup.get_text(separator=' ')

        # Прибираємо зайві пробіли та порожні рядки
        lines = (line.strip() for line in clean_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        final_text = '\n'.join(chunk for chunk in chunks if chunk)

        return final_text

    except Exception as e:
        print(f"Помилка при завантаженні тексту: {e}")
        return None

url_input = input("Введіть посилання на сайт (з http/https): ")
text = get_text_from_url(url_input)
text = re.sub(r'\s', ' ', text)

if text:
    n = len(text)
    counts = Counter(text)

    print(f"\nТекст успішно отримано! Довжина: {n} символів.")

    print("\nОберіть тип даних (одиниць виміру):")
    print("1. Біти (основа 2)")
    print("2. Ніти (основа e)")
    print("3. Діти (основа 10)")
    choice = input("Ваш вибір (1/2/3): ")

    if choice == '2':
        base = math.e
        unit = "нит"
    elif choice == '3':
        base = 10
        unit = "дит"
    else:
        base = 2
        unit = "бит"

    entropy = 0
    print("\n" + "-" * 40)
    print(f"{'Символ':<10} | {'Кількість':<10} | {'Вірогідність':<12}")
    print("-" * 40)

    for i, (char, count) in enumerate(sorted(counts.items(), key=lambda item: item[1], reverse=True)):
        p = count / n
        entropy -= p * math.log(p, base)
        if i < 10:
            display_char = repr(char)
            print(f"{display_char:<10} | {count:<10} | {p:<12.4f}")

    info_amount = n * entropy

    print("-" * 40)
    print(f"Символів тексту: {n}")
    print(f"Кількість унікальних символів: {len(counts)}")
    print(f"Ентропія: {entropy:.4f} {unit}/символ")
    print(f"Кількість інформації: {info_amount:.4f} {unit}")
else:
    print("Не вдалося обробити текст за цим посиланням.")