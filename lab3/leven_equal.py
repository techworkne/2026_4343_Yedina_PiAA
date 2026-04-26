rep, ins, dele = [int(x) for x in input().split()]

first = list(input().strip())
second = list(input().strip())

first_len = len(first)
second_len = len(second)

table = [ [0]*(second_len+1) for _ in range(first_len+1) ]

print(f"строка A: {first}, длина = {first_len}, строки")
print(f"строка B: {second}, длина = {second_len}, столбцы")
print(f"стоимости: replace={rep}, insert={ins}, delete={dele}\n")

for i in range (1, first_len+1): table[i][0] = i*dele
for j in range (1, second_len+1): table[0][j] = j*ins

print("начальная таблица (базовые стоимости):")
for row in table:
    print(" ".join(f"{x:3d}" for x in row))
print()

for i in range(1, 1+first_len):
    for j in range(1, 1+second_len):

        if first[i-1] == second[j-1]:
            m = 0
        else:
            m = rep

        table[i][j] = min(
            table[i - 1][j] + dele,
            table[i][j - 1] + ins,
            table[i - 1][j - 1] + m
        )

        print(f"после обработки строки i={i} (символ A[{i-1}]='{first[i-1]}'):")
        for row in table:
            print(" ".join(f"{x:3d}" for x in row))
        print()


print(table[first_len][second_len])
