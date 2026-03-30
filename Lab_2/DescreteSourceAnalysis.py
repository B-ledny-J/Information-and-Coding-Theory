import numpy as np #pip install numpy
import math

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

def generate_joint_probability_matrix(m):
    """Генерує матрицю спільної появи розмірністю m x m."""
    matrix = np.random.rand(m, m)
    return matrix / matrix.sum()

def calculate_marginal_probabilities(joint_matrix):
    """Обчислює безумовні ймовірності первинного (A) та вторинного (B) алфавітів."""
    p_a = np.sum(joint_matrix, axis=1)  # Сума за рядками
    p_b = np.sum(joint_matrix, axis=0)  # Сума за стовпцями
    return p_a, p_b

def calculate_conditional_matrices(joint_matrix, matrix_a, matrix_b):
    """Обчислює матриці умовних ймовірностей P(B/A) та P(A/B)."""
    m = len(joint_matrix)
    # P(B/A) = P(A,B) / P(A)
    p_b_a = []
    for i in range(m):
        row = []
        for j in range(m):
            row.append(joint_matrix[i][j] / matrix_a[i])
        p_b_a.append(row)
    # P(A/B) = P(A,B) / P(B)
    p_a_b = []
    for j in range(m):
        col = []
        for i in range(m):
            col.append(joint_matrix[i][j] / matrix_b[j])
        p_a_b.append(col)
    return p_a_b, p_b_a

def calculate_entropy(matrix, base):
    """Обчислює ентропію для заданого розподілу ймовірностей."""
    mask = matrix > 0
    entropy = 0 - np.sum(matrix[mask] * (np.log(matrix[mask]) / np.log(base))) # За формулою зміни бази логарифма
    return entropy

def calculate_conditional_entropy(cond_matrix, prob_matrix, base):
    """Обчислює умовну ентропію"""

    cond_matrix = np.array(cond_matrix)
    prob_matrix = np.array(prob_matrix)

    log_cond = np.zeros_like(cond_matrix)
    mask = cond_matrix > 0
    log_cond[mask] = np.log(cond_matrix[mask]) / np.log(base)

    inner = cond_matrix * log_cond
    entropy = 0 - np.sum(prob_matrix * np.sum(inner, axis=1))
    return entropy

def display_results(m, unit, p_ab, p_a, p_b, p_b_a, p_a_b, h_ab, h_a_b, h_b_a, h_a, h_b):
    """Функція для виведення результатів на екран"""
    print(f"\n--- Результати дослідження (Розмірність m={m}) ---")

    print("\n1. Матриця спільної появи P(A, B):")
    print(np.round(p_ab, 4))

    print("\n2. Безумовні ймовірності первинного алфавіту P(A):")
    print(np.round(p_a, 4))

    print("\n3. Безумовні ймовірності вторинного алфавіту P(B):")
    print(np.round(p_b, 4))

    print("\n4. Матриця умовних ймовірностей P(B/A):")
    print(np.round(p_b_a, 4))

    print("\n5. Матриця умовних ймовірностей P(A/B):")
    print(np.round(p_a_b, 4))

    print("\n--- Обчислення ентропії ---")
    print(f"H(A, B) = {h_ab:.4f} {unit}/символ")
    print(f"H(A)    = {h_a:.4f} {unit}/символ")
    print(f"H(B)    = {h_b:.4f} {unit}/символ")
    print(f"H(B/A)  = {h_b_a:.4f} {unit}/символ")
    print(f"H(A/B)  = {h_a_b:.4f} {unit}/символ")

m = 8
p_ab = generate_joint_probability_matrix(m) # Формування матриці спільної появи
p_a, p_b = calculate_marginal_probabilities(p_ab) # Отримання безумовних ймовірностей
p_a_b, p_b_a = calculate_conditional_matrices(p_ab, p_a, p_b) # Обчислення умовних ймовірностей
base, unit = get_base_unit()
# Розрахунок сумісної ентропії
h_ab = calculate_entropy(p_ab, base)
# Розрахунок безумовних ентропій
h_a = calculate_entropy(p_a, base)
h_b = calculate_entropy(p_b, base)
# Розрахунок умовних ентропій
h_a_b = calculate_conditional_entropy(p_a_b, p_b, base)
h_b_a = calculate_conditional_entropy(p_b_a, p_a, base)
display_results(m, unit, p_ab, p_a, p_b, p_b_a, p_a_b, h_ab, h_a_b, h_b_a, h_a, h_b) # Вивід інформації