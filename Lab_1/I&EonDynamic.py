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
        return re.sub(r'\s', ' ', clean_text)

    except Exception as e:
        print(f"Помилка при завантаженні тексту: {e}")
        return None

def get_base_unit():
    print("\nОберіть одиницю виміру:")
    print("1. Біти (основа 2)")
    print("2. Ніти (основа e)")
    print("3. Діти (основа 10)")
    choice = input("Ваш вибір (1/2/3): ")

    if choice == '2':
        base = math.e
        unit = "ніт"
    elif choice == '3':
        base = 10
        unit = "діт"
    else:
        base = 2
        unit = "біт"
    return base, unit

def process_statistics(text, base):
    entropy = 0
    n = len(text)
    counts = Counter(text)
    unique_count = len(counts)
    stats_list = []
    sorted_items = sorted(counts.items(), key=lambda item: item[1], reverse=True)

    for i, (char, count) in enumerate(sorted_items):
        p = count / n
        entropy -= p * math.log(p, base)
        if i < 10:
            stats_list.append((repr(char), count, p))

    info_amount = n * entropy
    return n, unique_count, entropy, info_amount, stats_list

def display_report(n, unique_count, entropy, info_amount, unit, stats_list):
    print("\n" + "-" * 40)
    print(f"{'Символ':<10} | {'Кількість':<10} | {'Частота':<12}")
    print("-" * 40)
    for char, count, p in stats_list:
        print(f"{char:<10} | {count:<10} | {p:<12.4f}")

    print("-" * 40)
    print(f"Довжина тексту: {n}")
    print(f"Кількість унікальних символів у тексті: {unique_count}")
    print(f"Ентропія: {entropy:.4f} {unit}/символ")
    print(f"Кількість інформації: {info_amount:.4f} {unit}")

url_input = input("Введіть посилання на сайт (з http/https): ")
text = get_text_from_url(url_input)

if text:
    base, unit = get_base_unit()
    n, counts, entropy, info_amount, top_10 = process_statistics(text, base)
    print(f"\nТекст успішно отримано!")
    display_report(n, counts, entropy, info_amount, unit, top_10)
else:
    print("Не вдалося обробити текст за цим посиланням.")
    exit()