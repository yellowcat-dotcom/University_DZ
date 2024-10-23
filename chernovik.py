# Исходные данные
profit_per_box = 35_000  # прибыль с одного ящика
loss_per_box = 56_000  # убыток за не проданный ящик
research_cost = 15_000  # стоимость исследования

# Вероятности продажи до и после исследований
probabilities_before = [0.45, 0.35, 0.2]  # для 11, 12 и 13 ящиков
probabilities_after = [0.4, 0.35, 0.25]  # для 11, 12 и 13 ящиков


# Определяем функцию расчета ожидаемой прибыли
def expected_profit(num_boxes, probabilities):
    outcomes = [11, 12, 13]  # возможное количество проданных ящиков
    total_profit = 0

    for i, sold in enumerate(outcomes):
        if num_boxes <= sold:
            total_profit += num_boxes * profit_per_box * probabilities[i]
        else:
            total_profit += (sold * profit_per_box - (num_boxes - sold) * loss_per_box) * probabilities[i]

    return total_profit


# Ожидаемая прибыль до исследований
profit_11_before = expected_profit(11, probabilities_before)
profit_12_before = expected_profit(12, probabilities_before)
profit_13_before = expected_profit(13, probabilities_before)

# Ожидаемая прибыль после исследований
profit_11_after = expected_profit(11, probabilities_after) - research_cost
profit_12_after = expected_profit(12, probabilities_after) - research_cost
profit_13_after = expected_profit(13, probabilities_after) - research_cost

# Выводим результаты
print(f"Ожидаемая прибыль при закупке 11 ящиков до исследований: {profit_11_before} рублей")
print(f"Ожидаемая прибыль при закупке 12 ящиков до исследований: {profit_12_before} рублей")
print(f"Ожидаемая прибыль при закупке 13 ящиков до исследований: {profit_13_before} рублей\n")

print(f"Ожидаемая прибыль при закупке 11 ящиков после исследований: {profit_11_after} рублей")
print(f"Ожидаемая прибыль при закупке 12 ящиков после исследований: {profit_12_after} рублей")
print(f"Ожидаемая прибыль при закупке 13 ящиков после исследований: {profit_13_after} рублей")

# Оптимальное решение
max_profit_before = max(profit_11_before, profit_12_before, profit_13_before)
max_profit_after = max(profit_11_after, profit_12_after, profit_13_after)

if max_profit_after > max_profit_before:
    print(
        f"\nПроведение исследования выгодно. Оптимальная стратегия: закупать {13 if max_profit_after == profit_13_after else 12 if max_profit_after == profit_12_after else 11} ящиков.")
else:
    print(
        f"\nПроведение исследования невыгодно. Оптимальная стратегия: закупать {13 if max_profit_before == profit_13_before else 12 if max_profit_before == profit_12_before else 11} ящиков.")
