import math
import random

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


def generate_matrix(size, sum_axis):
    """
    sum_axis=0: сума за стовпцями = 1 (для P(A|B))
    sum_axis=1: сума за рядками = 1 (для P(B|A))
    """
    matrix = [[random.random() for _ in range(size)] for _ in range(size)]
    if sum_axis == 1:  # По рядках
        for i in range(size):
            s = sum(matrix[i])
            matrix[i] = [x / s for x in matrix[i]]
    else:  # По стовпцях
        for j in range(size):
            s = sum(matrix[i][j] for i in range(size))
            for i in range(size):
                matrix[i][j] /= s
    return matrix

size = 8
t = 0.001
base, unit_name = get_base_unit()

# 1. Формування безумовних ймовірностей (рівномірний розподіл)
p_a = [[1.0 / size for _ in range(size)]]
p_b = [[1.0 / size] for _ in range(size)]

# 2. Генерація матриць умовних ймовірностей
matrix_ab = generate_matrix(size, sum_axis=0)  # P(A/B) сума по стовпцях = 1
matrix_ba = generate_matrix(size, sum_axis=1)  # P(B/A) сума по рядках = 1

# 3. Обчислення ентропій
h_a = -sum(p * math.log(p, base) for p in p_a[0])
h_b = -sum(p[0] * math.log(p[0], base) for p in p_b)

# H(B/A)
h_ba = 0
for i in range(size):
    row_entropy = -sum(p_ba * math.log(p_ba, base) for p_ba in matrix_ba[i] if p_ba > 0)
    h_ba += p_a[0][i] * row_entropy

# H(A/B)
h_ab = 0
for j in range(size):
    column_j = [matrix_ab[i][j] for i in range(size)]
    col_entropy = -sum(p_ab * math.log(p_ab, base) for p_ab in column_j if p_ab > 0)
    h_ab += p_b[j][0] * col_entropy

# 4. Взаємна інформація та пропускна здатність
i_ab = h_a - h_ab
capacity = i_ab/t

# --- ВИВІД РЕЗУЛЬТАТІВ ---
print(f"Одиниця виміру: {unit_name}")

print("\nМатриця P(B/A):")
for row in matrix_ba:
    print([round(x, 3) for x in row])

print("\nМатриця P(A/B):")
for row in matrix_ab:
    print([round(x, 3) for x in row])

print("\nМатриця P(A):")
for row in p_a:
    print([round(x, 3) for x in row])

print("\nМатриця P(B):")
for row in p_b:
    print([round(x, 3) for x in row])

print(f"\nРезультати обчислень:")
print(f"H(A)   = {h_a:.4f} {unit_name}/символ")
print(f"H(B)   = {h_b:.4f} {unit_name}/символ")
print(f"H(B/A) = {h_ba:.4f} {unit_name}/символ")
print(f"H(A/B) = {h_ab:.4f} {unit_name}/символ")
print(f"I(A,B) = {i_ab:.4f} {unit_name}/символ")
print(f"C = {capacity:.4f} {unit_name}/секунду")