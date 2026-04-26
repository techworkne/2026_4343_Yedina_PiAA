def LCS(str1, str2):
    m = len(str1)
    n = len(str2)
    lcs = [[0]*(n+1) for _ in range(1+m)]
    maxlen = 0
    endpos = 0

    # 0, i == 0 || j == 0
    # lcs[i-1][j-1] + 1, str1[i] == str[j]

    print(f"строка A: {str1}, длина = {m}, строки")
    print(f"строка B: {str2}, длина = {n}, столбцы")

    for i in range(1, m):
        lcs[i][0] = 0
    for j in range(1, n):
        lcs[0][j] = 0

    for i in range (1, m+1):
        for j in range (1, n+1):
            if str1[i-1] == str2[j-1]:
                lcs[i][j] = lcs[i-1][j-1] + 1
                if lcs[i][j] > maxlen:
                    maxlen = lcs[i][j]
                    endpos = i
                    print(f"\n\nновая подстрока: str1[{i-1}]='{str1[i-1]}' == str2[{j-1}]='{str2[j-1]}',\n lcs[{i}][{j}]={lcs[i][j]}, maxlen={maxlen}, endpos={endpos}")
            else:
                lcs[i][j] = 0
        print(f"\nсостояние после i={i} (символ '{str1[i-1]}'):")
        for row in lcs[:i+1]:
            print(" ".join(f"{x:2d}" for x in row))
        print()

    if maxlen > 0:
        longsub = str1[endpos - maxlen : endpos]
        return longsub, maxlen
    else:
        return "Общих подстрок не существует", 0


str1 = "vmva"
str2 = "va"

print( LCS(str1, str2) )
