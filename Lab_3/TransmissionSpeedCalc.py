import math

k = 1 + 10  # Номер команди 1

# Ймовірності геом. прогр.
probs = [(1 / 2) ** i for i in range(1, k)]
probs.append(1 - sum(probs))

# Тривалість символів
durations = [i for i in range(1, k + 1)]

# Середня тривалість для рівноймовріних символів
avg_tau_equal = sum(durations) / k

# Середня тривалість для геом. прогр.
avg_tau_geom = sum(p * t for p, t in zip(probs, durations))

# Ентропія для рівноймовірних символів
h_uniform = math.log2(k)

# Ентропія для геом. прогр
h_shannon = -sum(p * math.log2(p) for p in probs if p > 0)

# Швидкість передачі для рівноймовірних символів
R_equal = h_uniform / avg_tau_equal

# Швидкість передачі для геом. прогр.
R_geom = h_shannon / avg_tau_geom

print(f"--- Результати Частини 1.2 ---")
print(f"Ентропія Хартлі (Рівноймовірні символи): {h_uniform:.4f} біт/символ")
print(f"Швидкість передачі для рівноймовірних символів (R): {R_equal:.4f} біт/с")
print(f"Ентропія Шеннона (Геометрична прогресія): {h_shannon:.4f} біт/символ")
print(f"Швидкість передачі для геометричної прогресії (R): {R_geom:.4f} біт/с")
