import random

def gen(filename="test.txt"):
    n = int(input("колво городв: "))
    symmetric = int(input("симметричная? (1/0): ")) == 1
    filename = input("Имя файла для сохранения: ") or filename

    matrix = [[0] * n for _ in range(n)]

    if symmetric:
        for i in range(n):
            for j in range(i + 1, n):
                w = random.randint(1, 100)
                matrix[i][j] = w
                matrix[j][i] = w
    else:
        for i in range(n):
            for j in range(n):
                if i != j:
                    matrix[i][j] = random.randint(1, 100)

    with open(filename, 'w') as f:
        f.write(str(n) + "\n")
        for row in matrix:
            f.write(" ".join(map(str, row)) + "\n")

    print(f"сохранили в {filename}")


def main():
    gen()


if __name__ == "__main__":
    main()
