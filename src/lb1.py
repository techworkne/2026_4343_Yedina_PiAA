import matplotlib.pyplot as plt
import numpy as np

date_even_N = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
date_odd_N = np.array([3, 5, 7, 9, 11, 13, 15, 17, 19])

date_even = np.array([4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
date_odd = np.array([46, 645, 6093, 27748, 285319, 932962, 3166079, 16787837, 101750841])
plt.figure(figsize=(10, 6))

plt.yscale('log')
plt.plot(date_even_N, date_even, "m-*", linewidth=2, markersize=8, label='Чётные N')
plt.plot(date_odd_N, date_odd, "b-o",  linewidth=2, markersize=8, label='Нечётные N')
plt.grid(True, alpha=0.3)
plt.xlabel("N")
plt.ylabel("Количество операций")
plt.title("Зависимость числа операций от N")

plt.show()