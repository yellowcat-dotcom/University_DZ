# # Вероятности роста и отсутствия роста населения 3
# p_growth = 0.5
# p_no_growth = 0.5
#
# # Прибыль и убытки для каждого из решений
# big_expansion_growth = 250  # прибыль при большом расширении и росте населения
# big_expansion_no_growth = -120  # убыток при большом расширении и отсутствии роста населения
#
# small_expansion_growth = 90  # прибыль при малом расширении и росте населения
# small_expansion_no_growth = -45  # убыток при малом расширении и отсутствии роста населения
#
# no_expansion = 0  # отсутствие прибыли/убытков при отсутствии строительства
#
# # Ожидаемые значения для каждого решения
# expected_big_expansion = (p_growth * big_expansion_growth +
#                           p_no_growth * big_expansion_no_growth)
# expected_small_expansion = (p_growth * small_expansion_growth +
#                             p_no_growth * small_expansion_no_growth)
# expected_no_expansion = no_expansion  # всегда 0
#
# # Вывод результатов
# print(f"Ожидаемая прибыль при большом расширении: {expected_big_expansion} тыс. руб.")
# print(f"Ожидаемая прибыль при малом расширении: {expected_small_expansion} тыс. руб.")
# print(f"Ожидаемая прибыль при отсутствии работ: {expected_no_expansion} тыс. руб.")
#
# # Определим лучшее решение
# best_option = max(expected_big_expansion, expected_small_expansion, expected_no_expansion)
# if best_option == expected_big_expansion:
#     print("Лучшее решение: большое расширение")
# elif best_option == expected_small_expansion:
#     print("Лучшее решение: малое расширение")
# else:
#     print("Лучшее решение: не проводить работы")
#
#

# 4
# Входные данные
# prob_growth = 0.7  # Вероятность роста населения
# prob_no_growth = 0.3  # Вероятность отсутствия роста населения
#
# # Прибыль/убытки для большого расширения
# profit_large_expansion_growth = 250  # Прибыль при росте населения
# loss_large_expansion_no_growth = -120  # Убыток при отсутствии роста населения
#
# # Прибыль/убытки для малого расширения
# profit_small_expansion_growth = 90  # Прибыль при росте населения
# loss_small_expansion_no_growth = -45  # Убыток при отсутствии роста населения
#
# # Прибыль/убыток при отсутствии расширения (всегда 0)
# profit_no_expansion = 0
#
# # Ожидаемая денежная оценка (ОДО) для большого расширения
# expected_large_expansion = (
#     prob_growth * profit_large_expansion_growth +
#     prob_no_growth * loss_large_expansion_no_growth
# )
#
# # Ожидаемая денежная оценка (ОДО) для малого расширения
# expected_small_expansion = (
#     prob_growth * profit_small_expansion_growth +
#     prob_no_growth * loss_small_expansion_no_growth
# )
#
# # Ожидаемая денежная оценка (ОДО) для отсутствия расширения
# expected_no_expansion = profit_no_expansion
#
# # Определение наилучшего решения
# decisions = {
#     "Большое расширение": expected_large_expansion,
#     "Малое расширение": expected_small_expansion,
#     "Не расширяться": expected_no_expansion
# }
#
# # Находим максимальную ОДО и наилучшую стратегию
# best_decision = max(decisions, key=decisions.get)
# best_value = decisions[best_decision]
#
# # Вывод результатов
# print(f"Наилучшее решение: {best_decision}")
# print(f"Ожидаемая денежная оценка для наилучшего решения: {best_value:.2f} тыс. руб.")
