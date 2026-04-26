
first = input().strip()
second = input().strip()
n, m = len(first), len(second)


print(f"строка A: {first}, длина = {n}, строки")
print(f"строка B: {second}, длина = {m}, столбцы")

prev = list(range(m + 1))  # dp[0][j] = j
print(f"prev[0..{m}] (строка 0): {prev}")

for i in range(1, n + 1):
    curr = [i] + [0] * m   # dp[i][0] = i
    print(f"\ni = {i} (символ A[{i-1}]='{first[i-1]}')")
    print(f"curr[0] = {curr[0]}")
    for j in range(1, m + 1):
        cost = 0 if first[i-1] == second[j-1] else 1
        curr[j] = min(
            prev[j] + 1,    # удаление
            curr[j-1] + 1,  # вставка
            prev[j-1] + cost # замена
        )
        print(f"  j={j} (B[{j-1}]='{second[j-1]}'), cost={cost}, curr[{j}] = {curr[j]}")
    print(f"prev: {prev}")
    print(f"curr: {curr}")
    prev = curr

print(prev[m])
