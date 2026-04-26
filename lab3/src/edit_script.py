rep, ins, dele = [int(x) for x in input().split()]

first = list(input().strip())
second = list(input().strip())

first_len = len(first)
second_len = len(second)


print(f"строка A: {first}, длина = {first_len}, строки")
print(f"строка B: {second}, длина = {second_len}, столбцы")
print(f"стоимости: replace={rep}, insert={ins}, delete={dele}\n")

table = [ [0]*(second_len+1) for _ in range(first_len+1) ]

for i in range (1, first_len+1): table[i][0] = i*dele
for j in range (1, second_len+1): table[0][j] = j*ins

print("после базовой инициализации:")
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
    print(f"после строки i={i} (A[{i-1}]='{first[i-1]}'):")
    for row in table:
        print(" ".join(f"{x:3d}" for x in row))
    print()


print("редакционное предписание:")
i, j = first_len, second_len

prescripton = ""

while i > 0 or j > 0 :
    print(f"текущая позиция (i={i}, j={j}), cost={table[i][j]}")

    if i > 0 and j > 0 and table[i][j] == table[i-1][j-1] + (0 if first[i-1]==second[j-1] else rep):
        if first[i-1] == second[j-1]:
            prescripton += "M"
            print(f"совпадение: A[{i-1}]='{first[i-1]}' == B[{j-1}]='{second[j-1]}' -- M")
        else:
            prescripton += "R"
            print(f"замена: A[{i-1}]='{first[i-1]}' -- B[{j-1}]='{second[j-1]}' -- R")
        i -= 1
        j -= 1
    elif i > 0 and (table[i][j] == table[i - 1][j] + dele):
        prescripton += "D"
        i -= 1
        print(f"удаление: удаляем A[{i-1}]='{first[i-1]}' -- D")
    elif j > 0 and ( table[i][j] ==  table[i][j - 1] + ins):
        prescripton += "I"
        j -= 1
        print(f"вставка: вставляем B[{j-1}]='{second[j-1]}' -- I")

print(prescripton[::-1])
print("".join(first))
print("".join(second))
