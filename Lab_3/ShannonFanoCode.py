import math
from collections import Counter
import random

def generate_random_text_from_probs(data, length=200):
    """Генерує список символів згідно з ймовірностями."""
    text = []
    for item in data:
        count = round(item['p'] * length)
        text.extend([item['symbol']] * count)
    random.shuffle(text)
    return text[:length]

# --- Розрахунок ймовірностей ---
def get_probabilities_geometric(k=21):
    """Генерація ймовірностей за законом (1/2)^i"""
    probs = [(1 / 2) ** i for i in range(1, k)]
    probs.append(1 - sum(probs))  # Корекція суми до 1
    symbols = [f"s{i + 1}" for i in range(k)]
    return [{"symbol": s, "p": p, "code": ""} for s, p in zip(symbols, probs)]

def get_probabilities_from_text(text):
    """Розрахунок ймовірностей на основі введеного тексту (символи)"""
    total = len(text)
    counts = Counter(text)
    return [{"symbol": char, "p": count / total, "code": ""} for char, count in counts.items()]

def get_block_probabilities_from_text(text, block_size):
    """
    Розрахунок ймовірностей для агрегованих символів (блоків довжини block_size).
    Використовуємо неперекривні блоки.
    """
    if len(text) < block_size:
        return []

    blocks = [text[i:i + block_size] for i in range(0, len(text) - block_size + 1, block_size)]
    total = len(blocks)
    if total == 0:
        return []

    counts = Counter(blocks)
    return [{"symbol": block, "p": count / total, "code": ""} for block, count in counts.items()]

# --- Розрахунок ентропії ---
def calculate_entropy(data):
    return -sum(item['p'] * math.log2(item['p']) for item in data if item['p'] > 0)

# --- Сортування ---
def sort_data(data):
    return sorted(data, key=lambda x: x['p'], reverse=True)

# --- Алгоритм Шеннона-Фано ---
def assign_shannon_fano_codes(subset):
    if len(subset) <= 1:
        return

    total_p = sum(item['p'] for item in subset)
    acc_p = 0
    split_idx = 0
    min_diff = total_p

    for i in range(len(subset)):
        acc_p += subset[i]['p']
        diff = abs((total_p / 2) - acc_p)
        if diff < min_diff:
            min_diff = diff
            split_idx = i + 1
        else:
            break

    for i in range(len(subset)):
        subset[i]['code'] += "0" if i < split_idx else "1"

    assign_shannon_fano_codes(subset[:split_idx])
    assign_shannon_fano_codes(subset[split_idx:])

# --- Таблиця та довжини ---
def display_results(data, title=None):
    if title:
        print(f"\n=== {title} ===")
    print(f"\n{'Символ':<20} | {'Імовірність':<12} | {'Код':<20} | {'Довжина'}")
    print("-" * 70)
    for item in data:
        item['len'] = len(item['code'])
        print(f"{repr(item['symbol']):<20} | {item['p']:.8f} | {item['code']:<20} | {item['len']}")

# --- Середня довжина ---
def calculate_avg_length(data):
    return sum(item['p'] * len(item['code']) for item in data)

# --- Перевірка та оцінка ---
def verify_efficiency(entropy, avg_len, delta):
    diff = abs(avg_len - entropy)
    print("-" * 70)
    print(f"Ентропія H(X):          {entropy:.4f}")
    print(f"Середня довжина L_cp:   {avg_len:.4f}")
    print(f"Різниця (дельта):       {diff:.4f}")

    if diff <= delta:
        print(f"\n[УСПІХ] Ступінь близькості {diff:.4f} <= {delta}. Умова виконана.")
        return True
    else:
        print(f"\n[УВАГА] Різниця {diff:.4f} > {delta}. Потрібна оптимізація.")
        return False

# --- Кодування та декодування ---
def build_code_dict(data):
    """Побудова словника символ -> код"""
    return {item['symbol']: item['code'] for item in data}

def encode_text_blocks(text, code_dict, block_size=1):

    # Геометричний режим: text — список символів
    if isinstance(text, list):
        return "".join(code_dict[token] for token in text)

    # Звичайний режим: text — рядок
    bits = []
    if block_size == 1:
        for ch in text:
            bits.append(code_dict[ch])
    else:
        for i in range(0, len(text) - block_size + 1, block_size):
            block = text[i:i + block_size]
            bits.append(code_dict[block])

    return "".join(bits)

def decode_text_blocks(bitstring, code_dict):
    rev = {v: k for k, v in code_dict.items()}
    buffer = ""
    result = []

    for b in bitstring:
        buffer += b
        if buffer in rev:
            result.append(rev[buffer])
            buffer = ""

    if buffer:
        raise ValueError("Помилка декодування: залишок бітів не розпізнано.")

    return result   # список, а не рядок

# --- Блочна оптимізація (агреговані символи) ---
def optimize_with_blocks(text, delta, max_block_size):
    """
    Повторення кроків 2–10 для агрегованих символів (блоків).
    На цьому етапі: починаємо з block_size = 2, далі 3, 4, ...
    """
    for block_size in range(2, max_block_size + 1):
        print(f"\n\n##### БЛОЧНЕ КОДУВАННЯ: ДОВЖИНА БЛОКУ = {block_size} #####")

        data = get_block_probabilities_from_text(text, block_size)
        if not data:
            print("Недостатньо даних для побудови блоків цієї довжини.")
            continue

        data = sort_data(data)
        entropy = calculate_entropy(data)
        assign_shannon_fano_codes(data)
        display_results(data, title=f"Блоки довжини {block_size}")

        avg_len = calculate_avg_length(data)
        ok = verify_efficiency(entropy, avg_len, delta=delta)

        code_dict = build_code_dict(data)
        encoded = encode_text_blocks(text, code_dict, block_size=block_size)
        decoded = decode_text_blocks(encoded, code_dict)

        print(f"\nЗакодований текст (блоки {block_size}):")
        print(encoded)
        print(f"\nДекодований текст (блоки {block_size}):")
        print(decoded)

        if ok:
            print(f"\n[УСПІХ] Досягнуто потрібну близькість при довжині блоку {block_size}.")
            return

    print("\n[ПОВІДОМЛЕННЯ] Не вдалося досягти потрібної близькості для заданого діапазону довжин блоків.")

# --- ГОЛОВНЕ МЕНЮ ---
def main():

    delta = 0.1

    print("=== Кодування методом Шеннона-Фано ===")
    print("1. Геометрична прогресія (k=21)")
    print("2. Власна послідовність символів (текст)")

    choice = input("\nВиберіть режим: ")

    text = None

    if choice == '1':
        data = get_probabilities_geometric(21)
        # Генеруємо випадковий текст згідно з розподілом
        text = generate_random_text_from_probs(data, length=200)
        print("\nЗгенерований текст (геометричний розподіл):")
        print("".join(text))
    elif choice == '2':
        text = input("Введіть ваш текст: ")
        if not text:
            return
        data = get_probabilities_from_text(text)
    else:
        print("Невірний вибір.")
        return

    # Кроки 4–7
    data = sort_data(data)
    entropy = calculate_entropy(data)
    assign_shannon_fano_codes(data)
    display_results(data, title="Базове кодування (символи)")

    avg_len = calculate_avg_length(data)

    # Крок 10: кодування/декодування для базового алфавіту
    code_dict = build_code_dict(data)

    print("\n=== Кодування/декодування для базового коду ===")
    encoded = encode_text_blocks(text, code_dict, block_size=1)
    decoded = decode_text_blocks(encoded, code_dict)

    print("\nЗакодований текст:")
    print(encoded)
    print("\nДекодований текст:")
    print("".join(decoded))

    # Фінальна перевірка для базового коду
    ok = verify_efficiency(entropy, avg_len, delta)

    if ok:
        print("Завершення роботи системи...")
    else:
        print("\nПочинаємо блочну оптимізацію (агреговані символи)...")
        optimize_with_blocks(text, delta, max_block_size=4)

if __name__ == "__main__":
    main()