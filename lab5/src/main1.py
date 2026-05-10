class Vertex:
    def __init__(self, alpha=5):
        self.next = [None] * alpha  # список переходов в боре
        self.go = [None] * alpha  # список переходов в автомате
        self.sufflink = None
        self.dict_link = None
        self.pattern_ids = []


def num(c):
    return "ACGTN".index(c)


def build(patterns):
    root = Vertex()

    for idx, p in enumerate(patterns, start=1):
        v = root
        for i in range(len(p)):
            if v.next[num(p[i])] is None:
                v.next[num(p[i])] = Vertex()
            v = v.next[num(p[i])]
        v.pattern_ids.append(idx)

    from collections import deque
    queue = deque([root])
    root.sufflink = root
    root.dict_link = root

    while queue:
        v = queue.popleft()

        for c in range(5):
            child = v.next[c]
            if child:
                # cуффиксная ссылка для ребенка
                if v == root:
                    child.sufflink = root
                else:
                    child.sufflink = v.sufflink.go[c]

                # ближайший терминальный узел в цепочке суффиксов
                if child.sufflink.pattern_ids:
                    child.dict_link = child.sufflink
                else:
                    child.dict_link = child.sufflink.dict_link

                child.go[c] = child
                queue.append(child)

            if child:
                v.go[c] = child
            else:
                if v == root:
                    v.go[c] = root
                else:
                    v.go[c] = v.sufflink.go[c]
    return root


text = input().strip()
n = int(input())

patterns = []
for _ in range(n):
    patterns.append(input().strip())

results = []
root = build(patterns)

v = root
for i, char in enumerate(text):
    v = v.go[num(char)]

    # по терминальным узлам через сжатые ссылки
    temp = v
    while temp != root:
        if temp.pattern_ids:
            for p_id in temp.pattern_ids:
                results.append((i - len(patterns[p_id-1]) + 2, p_id))
        temp = temp.dict_link

results.sort()
for pos, p_id in results:
    print(pos, p_id)
