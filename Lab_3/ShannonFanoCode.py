import math
from collections import Counter


# --- КРОК 2: Розрахунок ймовірностей ---
def get_probabilities_geometric(k=21):
    """Генерація ймовірностей за законом (1/2)^i"""
    probs = [(1 / 2) ** i for i in range(1, k)]
    probs.append(1 - sum(probs))  # Корекція суми до 1
    symbols = [f"s{i + 1}" for i in range(k)]
    return [{"symbol": s, "p": p, "code": ""} for s, p in zip(symbols, probs)]


def get_probabilities_from_text(text):
    """Розрахунок ймовірностей на основі введеного тексту"""
    total = len(text)
    counts = Counter(text)
    # Створюємо список словників для кожного унікального символу
    return [{"symbol": char, "p": count / total, "code": ""} for char, count in counts.items()]


# --- КРОК 3: Розрахунок ентропії ---
def calculate_entropy(data):
    return -sum(item['p'] * math.log2(item['p']) for item in data if item['p'] > 0)


# --- КРОК 4: Сортування ---
def sort_data(data):
    return sorted(data, key=lambda x: x['p'], reverse=True)


# --- КРОК 5: Алгоритм Шеннона-Фано ---
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


# --- КРОК 6-7: Таблиця та довжини ---
def display_results(data):
    print(f"\n{'Символ':<8} | {'Імовірність':<12} | {'Код':<15} | {'Довжина'}")
    print("-" * 55)
    for item in data:
        item['len'] = len(item['code'])
        print(f"{item['symbol']:<8} | {item['p']:.8f} | {item['code']:<15} | {item['len']}")


# --- КРОК 8: Середня довжина ---
def calculate_avg_length(data):
    return sum(item['p'] * len(item['code']) for item in data)


# --- КРОК 9-10: Перевірка та оцінка ---
def verify_efficiency(entropy, avg_len, delta=0.1):
    diff = abs(avg_len - entropy)
    print("-" * 55)
    print(f"Ентропія H(X):          {entropy:.4f}")
    print(f"Середня довжина L_cp:   {avg_len:.4f}")
    print(f"Різниця (дельта):       {diff:.4f}")

    if diff <= delta:
        print(f"\n[УСПІХ] Ступінь близькості {diff:.4f} <= {delta}. Умова виконана.")
        return True
    else:
        print(f"\n[УВАГА] Різниця {diff:.4f} > {delta}. Потрібна оптимізація.")
        return False


# --- ГОЛОВНЕ МЕНЮ ---
def main():
    print("=== Аналізатор кодів Шеннона-Фано ===")
    print("1. Геометрична прогресія (k=21)")
    print("2. Власна послідовність символів (текст)")

    choice = input("\nВиберіть режим: ")

    if choice == '1':
        data = get_probabilities_geometric(21)
    elif choice == '2':
        text = input("Введіть ваш текст: ")
        if not text: return
        data = get_probabilities_from_text(text)
    else:
        print("Невірний вибір.")
        return

    # Виконання кроків
    data = sort_data(data)
    entropy = calculate_entropy(data)
    assign_shannon_fano_codes(data)
    display_results(data)

    avg_len = calculate_avg_length(data)

    # Фінальна перевірка
    if verify_efficiency(entropy, avg_len):
        print("Завершення роботи системи...")
    else:
        print("...Заглушка: Очікування додаткових інструкцій по оптимізації...")


if __name__ == "__main__":
    main()